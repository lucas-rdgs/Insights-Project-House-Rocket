import geopandas
from datetime import datetime
import folium
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px
from st_aggrid import GridOptionsBuilder, AgGrid
from st_aggrid.shared import GridUpdateMode

pd.options.display.float_format = '{:,.2f}'.format

st.set_page_config(page_title='House Rocket Company - Dashboard de Vendas', layout='centered', page_icon=':house:')


def page_header(title_widths):
    t1, t2 = st.columns(title_widths)
    t1.title('')
    t1.image('https://cdn-icons-png.flaticon.com/512/6760/6760104.png', use_column_width=True)
    t2.title("House Rocket Company - Dashboard de Vendas")
    return t1, t2


@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    return data


@st.cache(allow_output_mutation=True)
def get_geofile(url):
    geofile = geopandas.read_file(url)
    return geofile


@st.cache(allow_output_mutation=True)
def data_cleaning(data):
    # Convert date type
    # Convertendo os tipos de dados
    data['date'] = pd.to_datetime(data['date'])
    data['bathrooms'] = data['bathrooms'].astype(dtype='int64')
    data['floors'] = data['floors'].astype(dtype='int64')

    # Removing rows containing zeros
    # Removendo linhas que possuem zeros
    data = data[(data['bathrooms'] != 0) & (data['bedrooms'] != 0)]

    # Rounding up the values of columns "bathrooms" and "floors"
    # Arredondando os valores das colunas "banheiros" e "andares"
    data['bathrooms'] = data['bathrooms'].apply(np.ceil)
    data['floors'] = data['floors'].apply(np.ceil)

    # Creating columns converting square feet to square meters
    # Criando colunas convertendo pés quadrados para metros quadrados
    data['m2_living'] = data['sqft_living'].apply(lambda x: x / 10.7639).astype(dtype='int64')
    data['m2_lot'] = data['sqft_lot'].apply(lambda x: x / 10.7639).astype(dtype='int64')
    data['m2_above'] = data['sqft_above'].apply(lambda x: x / 10.7639).astype(dtype='int64')
    data['m2_basement'] = data['sqft_basement'].apply(lambda x: x / 10.7639).astype(dtype='int64')
    data['m2_living15'] = data['sqft_living15'].apply(lambda x: x / 10.7639).astype(dtype='int64')
    data['m2_lot15'] = data['sqft_lot15'].apply(lambda x: x / 10.7639).astype(dtype='int64')

    # Creating a columns "condition_description" with text description for the properties' condition
    data['condition_description'] = data['condition'].apply(lambda x: 'excellent' if x == 5 else
                                                                      'good' if x == 4 else
                                                                      'fair' if x == 3 else
                                                                      'poor' if x == 2 else
                                                                      'bad')

    # # - Criando a coluna "season" para cada data de venda dos imóveis
    # # intervalos para "dia do ano" para o hemisfério norte
    spring = range(80, 172)
    summer = range(172, 264)
    fall = range(264, 355)
    # # winter (inverno) para todos os outros dias

    data['season'] = data['date'].apply(lambda x: 'spring' if x.timetuple().tm_yday in spring else
                                                  'summer' if x.timetuple().tm_yday in summer else
                                                  'fall' if x.timetuple().tm_yday in fall else
                                                  'winter')

    return data


def get_data_sell(data):
    df_median = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()
    df_median.columns = ['zipcode', 'price_median']

    data = pd.merge(data, df_median, on='zipcode', how='inner')

    data_purchase = pd.DataFrame()
    data_purchase[['id', 'zipcode', 'purchase_price', 'price_median', 'condition']] = data[
        ['id', 'zipcode', 'price', 'price_median', 'condition']]

    for i in range(len(data_purchase)):
        if (data_purchase.loc[i, 'purchase_price'] < data_purchase.loc[i, 'price_median']) & (
                data_purchase.loc[i, 'condition'] >= 4):
            data_purchase.loc[i, 'status'] = 'Buy'
        else:
            data_purchase.loc[i, 'status'] = 'Do not buy'

    data = pd.merge(data, data_purchase[['id', 'status']], on='id', how='inner')

    df_median_season = data[['zipcode', 'season', 'price']].groupby(['zipcode', 'season']).median().reset_index()
    df_median_season.columns = ['zipcode', 'season', 'price_median_season']

    data = pd.merge(data, df_median_season, on=['zipcode', 'season'], how='inner')

    data_sell = pd.DataFrame()
    data_sell[['id', 'zipcode', 'season', 'price', 'price_median', 'condition', 'condition_description', 'status']] = \
        data[
            ['id', 'zipcode', 'season', 'price', 'price_median_season', 'condition', 'condition_description', 'status']]
    data_sell = data_sell[data_sell['status'] == 'Buy'].reset_index(drop=True)

    for i in range(len(data_sell)):
        if data_sell.loc[i, 'price'] < data_sell.loc[i, 'price_median']:
            data_sell.loc[i, 'sell_price'] = data_sell.loc[i, 'price'] * 1.3

        else:
            data_sell.loc[i, 'sell_price'] = data_sell.loc[i, 'price'] * 1.1

        data_sell.loc[i, 'gain'] = data_sell.loc[i, 'sell_price'] - data_sell.loc[i, 'price']

    data_sell.drop(columns=['status'], axis=1, inplace=True)

    return data_sell


def get_data_sell_full(data_sell, data):
    data_sell_full = pd.merge(data_sell, data[['id', 'lat', 'long', 'date', 'bedrooms',
                                               'bathrooms',  'sqft_living', 'floors', 'waterfront', 'yr_built']],
                              on='id', how='inner')

    return data_sell_full


def interactive_sell(df: pd.DataFrame):
    # st.header('Properties overview')
    st.header('Visão geral dos Imóveis')
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_column('price',
                             type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                             precision=2)
    options.configure_column('condition_description', header_name='condition_description')
    options.configure_column('sell_price', header_name='sell price')
    options.configure_column('sqft_living', header_name='living total area (sqft)')
    options.configure_column('waterfront', header_name='has waterview')
    options.configure_column('yr_built', header_name='year of construction')
    # options.configure_column('price_median',
    #                         type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
    #                         valueGetter="data.price_median.toLocaleString('en-US', {style: 'currency',
    #                         currency: 'USD', maximumFractionDigits:2})")
    options.configure_column('sell_price',
                             type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                             precision=2)
    options.configure_column('gain',
                             type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                             precision=2)

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )
    return selection


def region_overview(data_sell_full, geofile):
    # st.title('Region Overview')
    st.title('Visão Geral por Região')

    # tab1, tab2, tab3 = st.tabs(['Portfolio Density', 'Sell Price Density', 'Gain Density'])
    tab1, tab2, tab3 = st.tabs(['Densidade do Portfólio', 'Densidade de Preços de Venda', 'Densidade de Faturamento'])

    df1 = data_sell_full

    # Base map - Folium
    # Mapa base - Folium
    density_map = folium.Map(location=[data_sell_full['lat'].mean(), data_sell_full['long'].mean()],
                             default_zoom_start=15, width='100%')
    marker_cluster = MarkerCluster().add_to(density_map)
    # for name, row in df1.iterrows():
    #     iframe = folium.IFrame = (
    #         f"Sell price ${row['sell_price']:,.2f}. Purchased for ${row['price']:,.2f} on: {row['date']:%Y-%m-%d}.
    #         Condition: {row['condition_description']}. \nFeatures: {row['sqft_living']} sqft, "
    #         f"{row['bedrooms']} bedrooms, {row['bathrooms']:.0f} bathrooms, \nYear Built: {row['yr_built']}")
    #     popup = folium.Popup(iframe, min_width=200, max_width=200, min_height=200, max_height=200)
    #     folium.Marker(location=[row['lat'], row['long']], popup=popup, tooltip="Click to see property
    #                   information").add_to(marker_cluster)

    for name, row in df1.iterrows():
        iframe = folium.IFrame = (
            f"Preço de venda ${row['sell_price']:,.2f}. Comprado por ${row['price']:,.2f} em: {row['date']:%Y-%m-%d}. "
            f"Condição: {row['condition_description']}. \nAtributos: {row['sqft_living']} sqft, "
            f"{row['bedrooms']} quartos, {row['bathrooms']:.0f} banheiros, \nAno de contrução: {row['yr_built']}")
        popup = folium.Popup(iframe, min_width=200, max_width=200, min_height=200, max_height=200)
        folium.Marker(location=[row['lat'], row['long']], popup=popup,
                      tooltip="Clique para ver as informações do imóvel").add_to(marker_cluster)

    with tab1:
        # st.header('Portfolio Density')
        st.header('Densidade do Portfólio')
        folium_static(density_map)

    # Region Selling Price Map
    # Mapa de Preço de Venda por Região

    df2 = data_sell_full[['sell_price', 'zipcode', ]].groupby('zipcode').mean().reset_index()
    df2.columns = ['ZIP', 'PRICE']

    geofile = geofile[geofile['ZIP'].isin(df2['ZIP'].tolist())]
    geofile = pd.merge(geofile, df2[['ZIP', 'PRICE']], on='ZIP', how='inner')

    region_price_map = folium.Map(location=[data_sell_full['lat'].median(), data_sell_full['long'].median()],
                                  zoom_start=9.5, width='100%', height='90%')

    marker_cluster_price = MarkerCluster().add_to(region_price_map)
    # for name, row in data_sell_full.iterrows():
    #     iframe = folium.Iframe = (
    #         f"Selling price ${row['sell_price']:,.2f}. Purchased for ${row['price']:,.2f} on: {row['date']:%Y-%m-%d}.
    #         Condition: {row['condition_description']}. "
    #         f"Gain of ${row['gain']:,.2f} "
    #         f"Features: {row['sqft_living']} sqft,"
    #         f"{row['bedrooms']} bedrooms, {row['bathrooms']:.0f} bathrooms, \nYear Built: {row['yr_built']}")
    #     popup = folium.Popup(iframe, min_width=200, max_width=200, min_height=200, max_height=200)
    #     folium.Marker(location=[row['lat'], row['long']], popup=popup,
    #                   tooltip="Click to see property information").add_to(marker_cluster_price)

    for name, row in data_sell_full.iterrows():
        iframe = folium.Iframe = (
            f"Preço de venda ${row['sell_price']:,.2f}. Comprado por ${row['price']:,.2f} em: {row['date']:%Y-%m-%d}. "
            f"Condição: {row['condition_description']}. "
            f"Faturamento de ${row['gain']:,.2f} "
            f"Atributos: {row['sqft_living']} sqft,"
            f"{row['bedrooms']} quartos, {row['bathrooms']:.0f} banheiros, \nAno de construção: {row['yr_built']}")
        popup = folium.Popup(iframe, min_width=200, max_width=200, min_height=200, max_height=200)
        folium.Marker(location=[row['lat'], row['long']], popup=popup,
                      tooltip="Clique para ver as informações do imóvel").add_to(marker_cluster_price)

    # region_price_map.choropleth(data=df2,
    #                             geo_data=geofile,
    #                             columns=['ZIP', 'PRICE'],
    #                             key_on='feature.properties.ZIP',
    #                             fill_color='YlOrRd',
    #                             fill_opacity=0.7,
    #                             line_opacity=0.2,
    #                             legend_name='AVERAGE SELLING PRICE')

    region_price_map.choropleth(data=df2,
                                geo_data=geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                legend_name='PREÇO DE VENDA MÉDIO')

    style_function = lambda x: {'fillColor': '#ffffff',
                                'color': '#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000',
                                    'color': '#000000',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}

    # hover = folium.features.GeoJson(
    #         data=geofile,
    #         style_function=style_function,
    #         control=False,
    #         highlight_function=highlight_function,
    #         tooltip=folium.features.GeoJsonTooltip(
    #                 fields=['ZIP', 'PRICE'],
    #                 aliases=['Region Zipcode: ', 'Average Selling Price: '],
    #                 style="background-color: white; color: #333333; font-family: arial; font-size: 12px;
    #                 padding: 10px;",
    #                 localize=True
    #         )
    # )
    hover = folium.features.GeoJson(
            data=geofile,
            style_function=style_function,
            control=False,
            highlight_function=highlight_function,
            tooltip=folium.features.GeoJsonTooltip(
                    fields=['ZIP', 'PRICE'],
                    aliases=['Código postal: ', 'Preço de venda médio: '],
                    style="background-color: white; color: #333333; font-family: arial; font-size: 12px; "
                          "padding: 10px;",
                    localize=True
            )
    )
    region_price_map.add_child(hover)
    region_price_map.keep_in_front(hover)

    with tab2:
        # st.header('Selling Price Density')
        st.header('Densidade de Preço de Venda')
        folium_static(region_price_map)

    # Region Gain Map
    # Mapa de Faturamento por Região

    df3 = data_sell_full[['gain', 'zipcode', ]].groupby('zipcode').mean().reset_index()
    df3.columns = ['ZIP', 'GAIN']

    geofile = geofile[geofile['ZIP'].isin(df3['ZIP'].tolist())]
    geofile_gain = pd.merge(geofile, df3[['ZIP', 'GAIN']], on='ZIP', how='inner')

    region_gain_map = folium.Map(location=[data_sell_full['lat'].mean(), data_sell_full['long'].mean()],
                                 default_zoom_start=15)

    marker_cluster_gain = MarkerCluster().add_to(region_gain_map)
    # for name, row in data_sell_full.iterrows():
    #     iframe = folium.Iframe = (
    #         f"Selling price ${row['sell_price']:,.2f}. Purchased for ${row['price']:,.2f} on: {row['date']:%Y-%m-%d}.
    #         Condition: {row['condition_description']}. "
    #         f"Gain of ${row['gain']:,.2f} "
    #         f"Features: {row['sqft_living']} sqft,"
    #         f"{row['bedrooms']} bedrooms, {row['bathrooms']:.0f} bathrooms, \nYear Built: {row['yr_built']}")
    #     popup = folium.Popup(iframe, min_width=200, max_width=200, min_height=200, max_height=200)
    #     folium.Marker(location=[row['lat'], row['long']], popup=popup,
    #                   tooltip="Click to see property information").add_to(marker_cluster_gain)

    for name, row in data_sell_full.iterrows():
        iframe = folium.Iframe = (
            f"Preço de venda ${row['sell_price']:,.2f}. Comprado por ${row['price']:,.2f} em: {row['date']:%Y-%m-%d}. "
            f"Condição: {row['condition_description']}. "
            f"Faturamento de  ${row['gain']:,.2f} "
            f"Atributos: {row['sqft_living']} sqft,"
            f"{row['bedrooms']} quartos, {row['bathrooms']:.0f} banheiros, \nAno de Construção: {row['yr_built']}")
        popup = folium.Popup(iframe, min_width=200, max_width=200, min_height=200, max_height=200)
        folium.Marker(location=[row['lat'], row['long']], popup=popup,
                      tooltip="Clique para ver as informações do imóvel").add_to(marker_cluster_gain)

    # region_gain_map.choropleth(data=df3,
    #                            geo_data=geofile_gain,
    #                            columns=['ZIP', 'GAIN'],
    #                            key_on='feature.properties.ZIP',
    #                            fill_color='YlOrRd',
    #                            fill_opacity=0.7,
    #                            line_opacity=0.2,
    #                            legend_name='AVERAGE GAIN')

    region_gain_map.choropleth(data=df3,
                               geo_data=geofile_gain,
                               columns=['ZIP', 'GAIN'],
                               key_on='feature.properties.ZIP',
                               fill_color='YlOrRd',
                               fill_opacity=0.7,
                               line_opacity=0.2,
                               legend_name='FATURAMENTO MÉDIO')

    style_function = lambda x: {'fillColor': '#ffffff',
                                'color': '#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000',
                                    'color': '#000000',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}

    # hover_gain = folium.features.GeoJson(
    #     data=geofile_gain,
    #     style_function=style_function,
    #     control=False,
    #     highlight_function=highlight_function,
    #     tooltip=folium.features.GeoJsonTooltip(
    #         fields=['ZIP', 'GAIN'],
    #         aliases=['Region Zipcode: ', 'Average Gain: '],
    #         style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;",
    #         localize=True
    #     )
    # )

    hover_gain = folium.features.GeoJson(
        data=geofile_gain,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['ZIP', 'GAIN'],
            aliases=['Código postal: ', 'Faturamento médio: '],
            style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;",
            localize=True
        )
    )
    region_gain_map.add_child(hover_gain)
    region_gain_map.keep_in_front(hover_gain)

    with tab3:
        # st.header('Gain Density')
        st.header('Densidade de Faturamento')
        folium_static(region_gain_map)

    return None


def commercial_distribution(data_sell_full):
    # st.sidebar.title('Commercial Options')
    # st.title('Commercial Attributes')
    st.sidebar.title('Opções Comerciais')
    st.title('Atributos Comerciais')

    # # ---------- Average Price per Year
    # st.header('Average Price per Year')
    # ---------- Preço Médio por Ano
    st.header('Preço Médio por Ano')

    # Filters
    # Filtros
    min_year_built = int(data_sell_full['yr_built'].min())
    max_year_built = int(data_sell_full['yr_built'].max())

    # st.sidebar.subheader('Select Maximum Year Built')
    st.sidebar.subheader('Selecione o Ano de Construção Máximo')
    f_year_built = st.sidebar.slider('Year Built', min_value=min_year_built, max_value=max_year_built,
                                     value=max_year_built)

    # Data Selecion
    # Seleção de Dados
    df = data_sell_full.loc[data_sell_full['yr_built'] < f_year_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    # Plot
    # Gráfico
    fig = px.line(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # # ---------- Average Price per Day
    # st.header('Average Selling Price per Purchase Day')
    # ---------- Average Price per Day
    st.header('Preços de Venda Médios por Dia')

    # Filters
    # Filtros
    data_sell_full['date1'] = pd.to_datetime(data_sell_full['date']).dt.strftime('%Y-%m-%d')
    min_date = datetime.strptime(data_sell_full['date1'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(data_sell_full['date1'].max(), '%Y-%m-%d')

    f_date = st.sidebar.slider('Date', min_value=min_date, max_value=max_date, value=max_date)

    # Data Selection
    # Seleção de Dados
    data_sell_full['date'] = pd.to_datetime(data_sell_full['date'])
    df = data_sell_full.loc[data_sell_full['date'] < f_date]
    df = df[['date', 'price']].groupby('date').mean().reset_index()

    # Plot
    # Gráfico
    fig = px.line(df, x='date', y='price', title='Average Selling Price per Purchase Day')
    st.plotly_chart(fig, use_container_width=True)

    # # ---------- Histograms
    # st.header('Selling Price Distribution')
    # st.sidebar.subheader('Select Max Price')
    # ---------- Histogramas
    st.header('Distribuição dos Preços de Venda')
    st.sidebar.subheader('Selecione o Preço Máximo')

    # Filters
    # Filtros
    min_price = int(data_sell_full['price'].min())
    max_price = int(data_sell_full['price'].max())
    avg_price = int(data_sell_full['price'].mean())

    # f_price = st.sidebar.slider('Selling Price', min_value=min_price, max_value=max_price, value=avg_price)
    f_price = st.sidebar.slider('Preço de Venda', min_value=min_price, max_value=max_price, value=avg_price)

    # Data Selection
    # Seleção de Dados
    df = data_sell_full.loc[data_sell_full['price'] < f_price]

    # Plot
    # Gráfico
    fig = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)

    return None


def attributes_distribution(data_sell_full):
    # ===============================================
    # Distribuição dos imóveis por categorias físicas
    # ===============================================

    # st.sidebar.title('House Attributes Options')
    # st.sidebar.title('Attributes Options')
    # st.title('House Attributes')

    st.sidebar.title('Opções de Atributos dos Imóveis')
    st.sidebar.title('Opções de Atributos')
    st.title('Atributos dos Imóveis')

    # # Filters
    # f_bedrooms = st.sidebar.selectbox('Max number of bedrooms', data_sell_full['bedrooms'].sort_values().unique(),
    #                                   index=(len(data_sell_full['bedrooms'].sort_values().unique()) - 1))
    #
    # f_bathrooms = st.sidebar.selectbox('Max number of bathrooms', data_sell_full['bathrooms'].sort_values().unique(),
    #                                    index=(len(data_sell_full['bathrooms'].sort_values().unique()) - 1))
    #
    # f_floors = st.sidebar.selectbox('Max number of floors', data_sell_full['floors'].sort_values().unique(),
    #                                 index=len(data_sell_full['floors'].sort_values().unique()) - 1)
    #
    # # f_waterview = st.sidebar.checkbox('Only houses with waterview')

    # Filtros
    f_bedrooms = st.sidebar.selectbox('Número máximo de quartos', data_sell_full['bedrooms'].sort_values().unique(),
                                      index=(len(data_sell_full['bedrooms'].sort_values().unique()) - 1))

    f_bathrooms = st.sidebar.selectbox('Número máximo de banheiros', data_sell_full['bathrooms'].sort_values().unique(),
                                       index=(len(data_sell_full['bathrooms'].sort_values().unique()) - 1))

    f_floors = st.sidebar.selectbox('Número máximo de andares', data_sell_full['floors'].sort_values().unique(),
                                    index=len(data_sell_full['floors'].sort_values().unique()) - 1)

    # f_waterview = st.sidebar.checkbox('Apenas imóveis com vista para água')

    c1, c2 = st.columns(2)

    # # Houses per bedrooms
    # c1.header('Houses per number of bedrooms')
    # df = data_sell_full.loc[data_sell_full['bedrooms'] < f_bedrooms]
    # fig = px.histogram(df, x='bedrooms', nbins=19)
    # c1.plotly_chart(fig, use_container_width=True)

    # # Houses per bathrooms
    # c2.header('Houses per number of bathrooms')
    # df = data_sell_full.loc[data_sell_full['bathrooms'] < f_bathrooms]
    # fig = px.histogram(df, x='bathrooms', nbins=19)
    # c2.plotly_chart(fig, use_container_width=True)
    #
    # # Houses per floors
    # c1, c2 = st.columns(2)
    # c1.header('Houses per number of floor')
    # df = data_sell_full.loc[data_sell_full['floors'] < f_floors]
    # fig = px.histogram(df, x='floors', nbins=19)
    # c1.plotly_chart(fig, use_container_width=True)
    #
    # # Houses per waterview
    # c2.header('Houses with of without waterview')
    # if f_waterview:
    #     df = data_sell_full[data_sell_full['waterfront'] == 1]
    # else:
    #     df = data_sell_full.copy()

    # Imóveis por número de quartos
    c1.header('Imóveis por número de quartos')
    df = data_sell_full.loc[data_sell_full['bedrooms'] < f_bedrooms]
    fig = px.histogram(df, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # Imóveis por número de banheiros
    c2.header('Imóveis por número de banheiros')
    df = data_sell_full.loc[data_sell_full['bathrooms'] < f_bathrooms]
    fig = px.histogram(df, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

    # Imóveis por número de andares
    c1, c2 = st.columns(2)
    c1.header('Imóveis por número de andares')
    df = data_sell_full.loc[data_sell_full['floors'] < f_floors]
    fig = px.histogram(df, x='floors', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # Imóveis com vista para a água
    c2.header('Imóveis com vista para água')
    if f_waterview:
        df = data_sell_full[data_sell_full['waterfront'] == 1]
    else:
        df = data_sell_full.copy()

    fig = px.histogram(df, x='waterfront', nbins=3)
    c2.plotly_chart(fig, use_container_width=True)

    return None


if __name__ == "__main__":
    # --Data Extraction
    # Get data

    # --Extração de Dados
    # Carregar Dados
    path = 'kc_house_data.csv'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    data = get_data(path)
    title_widths = (0.15, 0.85)

    data = data_cleaning(data)
    data_sell = get_data_sell(data)
    data_sell_full = get_data_sell_full(data_sell, data)

    # Get geofile
    # Carregar geofile
    geofile = get_geofile(url)

    page_header(title_widths)
    selection = interactive_sell(df=data_sell_full[['id', 'zipcode', 'season', 'price', 'condition_description',
                                                    'sell_price', 'gain', 'bedrooms', 'bathrooms', 'sqft_living',
                                                    'floors', 'waterfront', 'yr_built']])
    region_overview(data_sell_full, geofile)

    commercial_distribution(data_sell_full)

    attributes_distribution(data_sell_full)
