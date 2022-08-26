import streamlit as st

st.set_page_config(page_title='House Rocket Company', layout='wide', page_icon=':house:')

st.markdown('# <center>Projeto de Insights - House Rocket</center>', unsafe_allow_html=True)

c1, c2 = st.columns((1, 3))
with c2:
    st.image('https://thumbs.dreamstime.com/b/classic-view-famous-painted-ladies-san-francisco-162287344.jpg',
             width=600)

st.sidebar.success('Selecione um dashboard acima')

st.header('1. Questão de negócio')
st.subheader('1.1 Sobre a empresa')
st.markdown('<p style="text-align: justify">A House Rocket é uma empresa digital fictícia de empreendimentos '
            'imobiliários. Seu modelo de negócios se define por encontrar oportunidades de compra e venda de imóveis no'
            ' estado de Washington, EUA, através de tecnologia. A principal estratégia da companhia é a compra de '
            'imóveis com ótima localização e preços baixos para então revendê-los a preços com altas margens de '
            'lucro, passando em vezes por processos de renovações.</p>', unsafe_allow_html=True)


st.subheader('1.2 Sobre o projeto')
st.markdown('<p style="text-align: justify">Ao se analizar uma propriedade, observa-se vários atributos tais como área '
            'total construída, números de quartos, banheiros e andares, anos de construção e reforma, código postais e '
            'outros. Tais informações tornam as propriedades mais ou menos atrativas a compradores e seus donos e, '
            'levando em conta também a sazonalidade, impactam de maneira '
            'significante seus preços.</p>\n'
            '<p style="text-align: justify">Assim, o objetivo deste projeto é fornecer aos parceiros de negócio as '
            'respostas a duas questões chave:</p>', unsafe_allow_html=True)
st.markdown('> - Quais imóveis deveriam ser compradas pela House Rocket?\n'
            '> - Quando e por qual preço os imóveis devem ser postos à venda?', unsafe_allow_html=True)

st.subheader('1.3. Visão geral do conjunto de dados')
st.markdown('<strong>Conjunto de dados bruto</strong>', unsafe_allow_html=True)
st.markdown('<p style="text-align: justify">O conjunto de dados bruto, ou seja, que não foi modificado por nenhum '
            'processo de limpeza e sem ação de nenhuma premissa, possui 21613 linhas e 21 colunas.</p>\n'
            'Estas 21 colunas são descritas abaixo:',
            unsafe_allow_html=True)
st.markdown('| **Coluna**        | Descrição |\n'
            '|:------------------|:--------------------------------------------------------------------------------|\n'
            '| **id**            | Código único identificador do imóvel vendido |\n'
            '| **date**          | Data de venda do imóvel |\n'
            '| **price**         | Preço de venda da propriedade |\n'
            '| **bedrooms**      | Número de quartos |\n'
            '| **bathrooms**     | Número de banheiros |\n'
            '| **sqft_living**   | Área, em pés quadrados, de área construída |\n'
            '| **sqft_lot**      | Área, em pés quadrados, de área do lote |\n'
            '| **floors**        | Número de andares |\n'
            '| **waterfront**    | Vista para água. Caso o valor seja 1, o imóvel possui vista para a costa. O valor '
            '0 indica que o imóvel não possui vista para a costa |\n'
            '| **view**          | Condição de vista do imóvel. 4 indica excelente; 3 indica ótimo; 2 indica regular; '
            '1 indica ruim; 0 indica péssima |\n'
            '| **condition**     | Condição do imóvel. 5 excelente. 4 boa; 3 regular; 2 ruim; 1 péssima |\n'
            '| **grade**         | Índice de 1 a 13, onde 1-3 peca em construção e design; 7 possui um nível médio de '
            'construção e design; 11-13 possui alta qualidade de construção e design |\n'
            '| **sqft_above**    | Área, em pés quadrados, dos andares a partir do térreo |\n'
            '| **sqft_basement** | Área, em pés quadrados, do porão, caso haja |\n'
            '| **yr_built**      | Ano de construção do imóvel |\n'
            '| **yr_renovated**  | Ano da última reforma do imóvel, caso haja |\n'
            '| **zipcode**       | Código postal |\n'
            '| **lat**           | Latitude, em graus |\n'
            '| **long**          | Longitude, em graus |\n'
            '| **sqft_living15** | Área, em pés quadrados, da área construída dos 15 vizinhos mais próximos |\n'
            '| **sqft_lot15**    | Área, em pés quadrados, da área total dos 15 vizinhos mais próximos |',
            unsafe_allow_html=True)

st.markdown('')
st.header('2. Premissas do negócio')
st.markdown('<p style="text-align: justify">Para a elaboração deste trabalho, as seguintes premissas são adotadas:</p>',
            unsafe_allow_html=True)
st.markdown(' - O conjunto de dados não possui linhas com dados faltantes (NaN, "-" ou similares);\n'
            ' - A coluna "bathrooms" possui valores decimais, porque é considerado que "3/4 de banheiro" é um cômodo '
            'que não possui ou chuveiro ou banheira, sendo assim um banheiro recebe valor 1 quando possui pia, vaso '
            'sanitário, chuveiro e banheira. Neste trabalho serão considerados todos os banheiros como completos, e '
            'por isso os valores serão arredondados para o próximo valor inteiro;\n'
            ' - Semelhante à coluna "bathrooms", a coluna "floors" possui valores decimais. A mesma abordagem de '
            'arredondamento para o próximo valor inteiro será adotada;\n'
            ' - Apartamentos que possuírem valores zerados para número de quartos e banheiros serão excluídos.',
            unsafe_allow_html=True)

st.header('3. Planejamento da solução')
st.subheader('3.1 O método SAPE (Saída - Processo - Entrada)')
st.markdown('<strong>Saída (Produto final)</strong>', unsafe_allow_html=True)
st.markdown('Serão fornecidos dois relatórios:', unsafe_allow_html=True)
st.markdown('> - Relatório com as sugestões de compra de imóveis por um valor recomendado;\n'
            '> - Relatório com as sugestões de venda de imóveis por um valor recomendado.', unsafe_allow_html=True)

st.markdown('')
st.markdown('Ambos os relatórios estarão presentes em um único dashboard do Streamlit contendo:')
st.markdown('> - Tabela com informações sobre os imóveis e recomendação de compra e venda;\n'
            '> - Mapas descrevendo as densidades do portfólio e dos preços;\n'
            '> - Gráficos plotando os preços médios por anos e dias, ao longo da série histórica das listas de compra '
            'e venda;\n'
            '> - Histograma da distribuição dos preços de compra e venda;\n'
            '> - Gráficos com os atributos físicos dos imóveis, sendo quartos, banheiros, andares e presença ou não do '
            'imóvel à costa.', unsafe_allow_html=True)

st.markdown('')
st.markdown('Os relatórios terão filtros para exploração dos dados.', unsafe_allow_html=True)
st.markdown('<strong>Processo (Passo-a-passo)\n1. Extração dos dados (Extraction)</strong>', unsafe_allow_html=True)
st.markdown('> - Carregar o conjunto de dados bruto com a biblioteca pandas e armazenar em uma variável.',
            unsafe_allow_html=True)
st.markdown('<strong>2. Transformação dos dados (Transformation)</strong>', unsafe_allow_html=True)

st.markdown('')
st.markdown('2.1. Limpeza dos dados', unsafe_allow_html=True)
st.markdown('> - Conferir os dados faltantes da base de dados e excluir as linhas (PREMISSA);\n'
            '> - Conferir dados zerados nas colunas de andares, quartos e banheiros e excluí-los (PREMISSA);\n'
            '> - Arredondar os valores das colunas "bathrooms" e "floors" para o próximo valor inteiro (PREMISSA);\n'
            '> - Conferir os tipos das colunas e, se necessário, alterá-los.', unsafe_allow_html=True)

st.markdown('')
st.markdown('2.2. Criação de novas colunas', unsafe_allow_html=True)
st.markdown('> - Criar novas colunas convertendo pés quadrados em metros quadrados;\n'
            '> - Criar nova coluna com a condição dos imóveis em texto (boa, regular e ruim);\n'
            '> - Criar nova coluna com a estação do ano do imóvel.', unsafe_allow_html=True)

st.markdown('')
st.markdown('2.3. Seção de compra', unsafe_allow_html=True)
st.markdown('2.3.1. Construção de tabela de compra', unsafe_allow_html=True)
st.markdown('> - Agrupar os dados por região;\n'
            '> - Dentro de cada região, encontrar a mediana do preço dos imóveis;\n'
            '> - Criar nova coluna e nela sugerir que os imóveis que estão abaixo do preço mediano de cada região e '
            'que estejam em boas condições sejam comprados.', unsafe_allow_html=True)

st.markdown('')
st.markdown('2.4. Seção de venda', unsafe_allow_html=True)
st.markdown('2.4.1. Construção de tabela de venda', unsafe_allow_html=True)
st.markdown('- Agrupar os imóveis por região (zipcode) e por sazonalidade (estações do ano);\n'
            '- Dentro de cada região e sazonalidade, calcular a mediana de preços;\n'
            '- Criar nova coluna com as condições de venda:', unsafe_allow_html=True)
st.markdown('    > - Se o preço da compra for maior que a mediana da região+sazonalidade:<br/>'
            'O preço da venda será igual ao preço da compra + 10%.\n'
            '    > - Se o preço da compra for menor que a mediana da região+sazonalidade:<br/>'
            'O preço da venda será igual ao preço da compra + 30%.', unsafe_allow_html=True)

st.markdown('')
st.markdown('2.5. Construção do dashboard', unsafe_allow_html=True)
st.markdown('2.5.1. Tabelas', unsafe_allow_html=True)
st.markdown('- Inserir as tabelas de compra e venda desenvolvidas anteriormente no dashboard;\n'
            '- Calcular o preço médio dos imóveis de cada tabela;\n'
            '- Criar tabela de estatísticas descritivas para os imóveis de compra e venda', unsafe_allow_html=True)

st.markdown('2.5.2. Mapas', unsafe_allow_html=True)
st.markdown('- Criar mapa com a densidade de portfólio;\n'
            '- Criar mapa com a densidade de preços.\n'
            '- Criar mapa com a densidade do faturamento de cada imóvel, no dashboard de vendas.',
            unsafe_allow_html=True)

st.markdown('2.5.3. Gráficos', unsafe_allow_html=True)
st.markdown('Atributos comerciais:', unsafe_allow_html=True)
st.markdown('    > - Evolução dos preços ano a ano;\n'
            '    > - Evolução dos preços dia a dia;\n'
            '    > - Histograma de preços.', unsafe_allow_html=True)
st.markdown('Atributos físicos:', unsafe_allow_html=True)
st.markdown('    > - Distribuição de número de quartos;\n'
            '    > - Distribuição de número de banheiros;\n'
            '    > - Distribuição de número andares;\n'
            '    >- Distribuição de vista para costa.', unsafe_allow_html=True)

st.markdown('')
st.markdown('<strong>3. Carregamento dos dados (Loading)</strong>', unsafe_allow_html=True)
st.markdown('3.1. Validação de hipóteses', unsafe_allow_html=True)

st.markdown('')
st.markdown('3.2. Avaliação de insights para o negócio', unsafe_allow_html=True)
st.markdown('<strong>Entrada</strong>', unsafe_allow_html=True)
st.markdown('Os dados deste projeto foram retirados do portal Kaggle e estão disponíveis no link:',
            unsafe_allow_html=True)
st.markdown('[https://www.kaggle.com/datasets/harlfoxem/housesalesprediction](https://www.kaggle.com/datasets/'
            'harlfoxem/housesalesprediction)', unsafe_allow_html=True)


st.header('4. Testes de hipoteses e insights do negócio')
st.subheader('4.1. Hipóteses')
st.markdown('<p style="text-align: justify"> Foram testadas 10 hipóteses acerca do conjunto de dados dos imóveis, '
            'com seus resultados e descrições abaixo:</p>', unsafe_allow_html=True)
st.markdown('| Hipótese | Validação | Significado para o negócio |\n'
            '|:----------|:-----------|:----------------------------|\n'
            '| <strong>H1: </strong>Imóveis com porão possuem em média área total 20% maior | Verdadeira | A média de '
            'área total construída dos imóveis com porão é 20,13% maior que aqueles que não possuem este cômodo. Devem '
            'ser considerados visto que o aumento de área total é significativo. |\n'
            '| <strong>H2: </strong>Imóveis com reformas são em média 40% mais caros | Verdadeira | O preço médio dos '
            'imóveis que foram reformados é 43% em relação aos que nunca passaram por processos de renovação. É '
            'aconselhável comprar imóveis com condições boas para então reformá-los visando lucro na revenda. |\n'
            '| <strong>H3: </strong>Imóveis com até 2 quartos são em média 30% mais baratos. | Verdadeira | Os imóveis '
            'com menos de 2 quartos são em média 30% mais baratos que aqueles que possuem mais dormitórios. Estes '
            'imóveis são boa opção de portfólio com preços mais baixos. |\n'
            '| <strong>H4: </strong>Imóveis que possuem vista para água são em média 30% mais caros | Falsa | Imóveis '
            'com vista para a água são em média 214% mais caros. |\n'
            '| <strong>H5: </strong>Imóveis com data de construção menor que 1957 são em média 50% mais '
            'baratos | Falsa | Os imóveis mais antigos possuem pequena variação de preço médio comparado aos mais '
            'novos, construídos a partir de 1957, sendo apenas 2.83% mais barato. Quando comparado com outros '
            'atributos do portfólio, este possui menor significância. |\n'
            '| <strong>H6: </strong>O crescimento do preço dos imóveis Year over Year (YoY) é de 10% | Falsa | O preço'
            ' médio dos imóveis vendidos em 2015 são apenas 0.53% maiores que aqueles vendidos no ano anterior. Assim, '
            'este comportamento não deve ser levado em conta no estudo. |\n'
            '| <strong>H7: </strong>O crescimento do preço dos imóveis Month over Month (MoM) de 15% | Falsa | Entre '
            'os meses de maio/2014 e maio/2015, a variação do preço médio dos imóveis variou dentro de um intervalo de'
            ' -3% e 7% em relação ao mês anterior, nunca alcançando uma variação de 15%. |\n'
            '| <strong>H8: </strong>Imóveis com condição a partir de 3 são em média 40% mais caros que os imóveis com'
            ' condição 1. | Falsa | Imóveis com condições acima de 3, ou seja, os imóveis que são considerados "bons" '
            'ou melhores, possuem preço médio 60% maiores que aqueles com condições ruins. Portanto, estes imóveis '
            'possuem maior valor de mercado. |\n'
            '| <strong>H9: </strong>Imóveis com porão são em média 5% mais caros. | Falsa | Imóveis com porão, além de '
            'maiores em área total, são também 28% mais caros. Consequentemente, são imóveis mais bem avaliados. |\n'
            '| <strong>H10: </strong>Imóveis são vendidos no verão por um preço médio 15% maior que no '
            'inverno. | Falsa | A variação entre os preços médios dos imóveis vendidos no verão e no inverno é de'
            ' apenas 3%. Ou seja, não há variação significativa entre os preços nas duas estações. |\n',
            unsafe_allow_html=True)

st.subheader('4.2. Insights')
st.markdown('<p style="text-align: justify">A análise exploratória dos dados das propriedades disponíveis para compra '
            'e revenda pela House Rocket proporciona alguns insights:</p>', unsafe_allow_html=True)
st.subheader('Insight 1: Imóveis com vista para a água')
st.markdown('<p style="text-align: justify">O valor de mercado dos imóveis é fortemente influenciado pela sua '
            'localização, principalmente em relação à proximidade a grandes corpos d’água. Neste portfólio, as '
            'propriedades situadas à beira dos lagos presentes na região de Seattle, WA apresentam um preço médio '
            '214% maior que aquelas situadas distante das costas.</p>', unsafe_allow_html=True)
st.subheader('Insight 2: Imóveis que foram reformados')
st.markdown('<p style="text-align: justify">Reformas elevam consideravelmente o preço dos imóveis do portfólio '
            'analisado. Comparadas àquelas que não passaram por nenhum processo de renovação, as propriedades '
            'reformadas possuem preço em média 40% maiores.</p>', unsafe_allow_html=True)
st.subheader('Insight 3: Idade de construção dos imóveis')
st.markdown('<p style="text-align: justify">Foram analisadas as idades dos imóveis. A diferença entre o preço médio '
            'dos imóveis que foram constrídos antes e depois de 1957 (a mediana dos valores dos anos de contrução, '
            'que vão de 1900 a 2015) é de apenas 2.83%. Assim, esta variável não é significante comparada à influência '
            'dos outros atributos do conjunto de dados.</p>', unsafe_allow_html=True)


st.header('5. Resultados financeiros para o negócio')
st.markdown('<p style="text-align: justify">A partir das considerações sobre os imóveis, levando em conta as condições '
            'físicas, estação de compra e atributos físicos, são obtidos <strong>3872</strong> propriedades '
            'recomendadas para compra. As somas dos preços de compra e venda, além como o <strong>lucro total</strong> '
            'possível estão descritos na tabela abaixo: </p>', unsafe_allow_html=True)
st.markdown('|  Número de imóveis |  Preço de compra total  |   Preço de venda total  |   Faturamento total |\n'
            '| :-----------------:|:-----------------------:|:-----------------------:|:-------------------:|\n'
            '|        3872        |   $1.522.626.895,00     |    $1.959.734.476,70    |    $437.107.581,70  |',
            unsafe_allow_html=True)

st.markdown('')
st.markdown('<p style="text-align: justify">Evidentemente, devido à provável impossibilidade de adquirir todos os '
            'imóveis sugeridos imediatamente, devem ser levadas em conta fatores como localização, tamanho dos '
            'imóveis, recursos financeiros disponíveis e outros para diversificação do portfólio.</p>',
            unsafe_allow_html=True)

st.header('6. Conclusão')
st.markdown('<p style="text-align: justify">Este documento provê uma análise exploratória de um conjunto de dados de '
            'imóveis disponíveis para a compra. Por meio de uma empresa fictícia com modelo de negócio bem definido, '
            'foi possível apresentar um processo completo de limpeza, carregamento e transformação de dados. O '
            'conjunto bruto foi explicado, foram propostas premissas sobre os dados e, assim, os imóveis foram '
            'categorizados em "Comprar" ou "Não comprar". Para ajudar o público final deste estudo na análise e '
            'visualização das propriedades, foram desenvolvidos dois dashboards com tabelas, mapas e gráficos. '
            'Por fim, este documento trouxe os resultados financeiros para o negócio, apresentando o faturamento '
            'máximo do portfólio de imóveis.</p>', unsafe_allow_html=True)


st.header('7. Próximos passos')
st.markdown('<p style="text-align: justify">Este projeto pode ir além nas análises e visualizações já aqui '
            'desenvolvidas, incluindo intens como:</p>', unsafe_allow_html=True)
st.markdown('>- Inclusão de banheiros considerados decimais (como 3/4 de banheiro sendo um lavatório que não possui '
            'chuveiro ou banheiro), que foram arredondados como premissa neste trabalho;\n'
            '>- Refinamento do preço de venda dos imóveis, levando em conta não apenas o preço médio por região e a '
            'sazonalidade, mas também atributos físicos das propriedades;\n'
            '>- Análise e sugestão de renovações nos imóveis para ampliação do portfólio da empresa.',
            unsafe_allow_html=True)

st.markdown('')
st.header('8. Tecnologias')
st.markdown('<strong>Desenvolvimento do código</strong>', unsafe_allow_html=True)
st.markdown('[<img src="https://upload.wikimedia.org/wikipedia/commons/3/38/Jupyter_logo.svg" style="height: 50px"'
            ' align="left"/>](https://jupyter.org/) [<img src="https://upload.wikimedia.org/wikipedia/commons/1/1d/'
            'PyCharm_Icon.svg" style="height: 50px" '
            'align="left"/>](https://www.jetbrains.com/pt-br/pycharm/) [<img src="https://upload.wikimedia.org/'
            'wikipedia/commons/thumb/e/ed/Pandas_logo.svg/1200px-Pandas_logo.svg.png" ' 
            'style="height: 50px" align="left"/>](https://pandas.pydata.org/) [<img src="https://geopandas.org/en/'
            'latest/_images/geopandas_logo.png" style="height: 40px" '
            'align="left"/>](https://geopandas.org/en/stable/)', unsafe_allow_html=True)

st.markdown('')
st.markdown('<strong>Construção e publicação dos dashboards</strong>', unsafe_allow_html=True)
st.markdown('[<img src="https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.svg" '
            'style="height: 50px" align="left"/>](https://streamlit.io/) [<img src="https://blog.back4app.com/'
            'wp-content/uploads/2020/12/O-que-e-o-Heroku.png" style="height: 50px" align="left"/>](http://heroku.com)',
            unsafe_allow_html=True)

st.markdown('<br/>', unsafe_allow_html=True)
