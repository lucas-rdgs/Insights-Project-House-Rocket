# <center>Projeto de Insights - House Rocket</center>

<center><img src="https://thumbs.dreamstime.com/b/classic-view-famous-painted-ladies-san-francisco-162287344.jpg" align="center" style="height: 387.8px; width:600.0px;"/></center>

Clique no ícone para acessar os dashboards desenvolvidos neste projeto:<br/> 
[<img src="https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.svg" style="height: 50px"/>](https://lucas-rdgs-projeto-insights-house-rocket-homepage-fb24vy.streamlit.app/)<br/>

## 1. Questão de negócio

### 1.1. Sobre a empresa
<p align="justify">A House Rocket é uma empresa digital fictícia de empreendimentos imobiliários. Seu modelo de negócios se define por encontrar oportunidades de compra e venda de imóveis no estado de Washington, EUA, através de tecnologia. A principal estratégia da companhia é a compra de imóveis com ótima localização e preços baixos para então revendê-los a preços com altas margens de lucro, passando em vezes por processos de renovações.</p>

### 1.2. Sobre o projeto
<p align="justify">Ao se analizar uma propriedade, observa-se vários atributos tais como área total construída, números de quartos, banheiros e andares, anos de construção e reforma, código postais e outros. Tais informações tornam as propriedades mais ou menos atrativas a compradores e seus donos e, levando em conta também a sazonalidade, impactam de maneira significante seus preços.</p>
<p align="justify">Assim, o objetivo deste projeto é fornecer aos parceiros de negócio as respostas a duas questões chave:</p>

> - Quais imóveis deveriam ser compradas pela House Rocket?
> - Quando e por qual preço os imóveis devem ser postos à venda?

### 1.3. Visão geral do conjunto de dados
#### Conjunto de dados bruto
<p align="justify">O conjunto de dados bruto, ou seja, que não foi modificado por nenhum processo de limpeza e sem ação de nenhuma premissa, possui 21613 linhas e 21 colunas.</p>

Estas 21 colunas são descritas abaixo:

| **Coluna**        | Descrição                                                                                                                             |
|:-------------------|:---------------------------------------------------------------------------------------------------------------------------------------|
| **id**            | Código único identificador do imóvel vendido                                                                                                 |
| **date**          | Data de venda do imóvel                                                                                                |
| **price**         | Preço de venda da propriedade                                                                                                                  |
| **bedrooms**      | Número de quartos                                                                                                                     |
| **bathrooms**     | Número de banheiros                                                                                                                   |
| **sqft_living**   | Área, em pés quadrados, de área construída                                                                                            |
| **sqft_lot**      | Área, em pés quadrados, de área do lote                                                                                               |
| **floors**        | Número de andares                                                                                                                     |
| **waterfront**    | Vista para água. Caso o valor seja 1, o imóvel possui vista para a costa. O valor 0 indica que o imóvel não possui vista para a costa |
| **view**          | Condição de vista do imóvel. 4 indica excelente; 3 indica ótimo; 2 indica regular; 1 indica ruim; 0 indica péssima                                                                                                                                   |
| **condition**     | Condição do imóvel. 5 excelente. 4 boa; 3 regular; 2 ruim; 1 péssima                                                          |
| **grade**         | Índice de 1 a 13, onde 1-3 peca em construção e design; 7 possui um nível médio de construção e design; 11-13 possui alta qualidade de construção e design                                                                                    |
| **sqft_above**    | Área, em pés quadrados, dos andares a partir do térreo |
| **sqft_basement** | Área, em pés quadrados, do porão, caso haja                                                                                         |
| **yr_built**      | Ano de construção do imóvel                                                                                                           |
| **yr_renovated**  | Ano da última reforma do imóvel, caso haja                                                                                                   |
| **zipcode**       | Código postal                                                                                                                         |
| **lat**           | Latitude, em graus                                                                                                                    |
| **long**          | Longitude, em graus                                                                                                                   |
| **sqft_living15** | Área, em pés quadrados, da área construída dos 15 vizinhos mais próximos                                                                                                           |
| **sqft_lot15**    | Área, em pés quadrados, da área total dos 15 vizinhos mais próximos                                                                                                           |

## 2. Premissas do negócio
<p align="justify">Para a elaboração deste trabalho, as seguintes premissas são adotadas:</p>

- O conjunto de dados não possui linhas com dados faltantes (NaN, '-' ou similares);
- A coluna 'bathrooms' possui valores decimais, porque é considerado que "3/4 de banheiro" é um cômodo que não possui ou chuveiro ou banheira, sendo assim um banheiro recebe valor 1 quando possui pia, vaso sanitário, chuveiro e banheira. Neste trabalho serão considerados todos os banheiros como completos, e por isso os valores serão arredondados para o próximo valor inteiro;
- Semelhante à coluna 'bathrooms', a coluna 'floors' possui valores decimais. A mesma abordagem de arredondamento para o próximo valor inteiro será adotada;
- Apartamentos que possuírem valores zerados para número de quartos e banheiros serão excluídos.


## 3. Planejamento da solução
### 3.1 O método SAPE (Saída - Processo - Entrada)
#### Saída (Produto final)
Serão fornecidos dois relatórios:

- Relatório com as sugestões de compra de imóveis por um valor recomendado;
- Relatório com as sugestões de venda de imóveis por um valor recomendado.
    
Ambos os relatórios estarão presentes em um único dashboard do Streamlit contendo:

- Tabela com informações sobre os imóveis e recomendação de compra e venda;
- Mapas descrevendo as densidades do portfólio e dos preços;
- Gráficos plotando os preços médios por anos e dias, ao longo da série histórica das listas de compra e venda;
- Histograma da distribuição dos preços de compra e venda;
- Gráficos com os atributos físicos dos imóveis, sendo quartos, banheiros, andares e presença ou não do imóvel à costa.

Os relatórios terão filtros para exploração dos dados.

#### Processo (Passo-a-passo)
<strong>1. Extração dos dados (Extraction)</strong>
- Carregar o conjunto de dados bruto com a biblioteca Pandas e armazenar em uma variável.

<strong>2. Transformação dos dados (Transformation)</strong>

2.1. Limpeza dos dados

- Conferir os dados faltantes da base de dados e excluir as linhas;
- Conferir dados zerados nas colunas de andares, quartos e banheiros e excluí-los;
- Arredondar os valores das colunas 'bathrooms' e 'floors' para o próximo valor inteiro;
- Conferir os tipos das colunas e, se necessário, alterá-los;

2.2. Criação de novas colunas

- Criar novas colunas convertendo pés quadrados em metros quadrados;
- Criar nova coluna com a condição dos imóveis em texto (excelente, boa, regular, ruim e péssima);
- Criar nova coluna com a estação do ano da venda do imóvel.


2.3. Seção de compra

2.3.1. Construção de tabela de compra

- Agrupar os dados por região;
- Dentro de cada região, encontrar a mediana do preço dos imóveis;
- Criar nova coluna e nela sugerir que os imóveis que estão abaixo do preço mediano de cada região e que estejam em boas condições sejam comprados.


2.4. Seção de venda

2.4.1. Construção de tabela de venda

- Agrupar os imóveis por região (zipcode) e por sazonalidade (estações do ano);
- Dentro de cada região e sazonalidade, calcular a mediana de preços;
- Criar nova coluna com as condições de venda:

    - Se o preço da compra for maior que a mediana da região+sazonalidade:<br/>
      O preço da venda será igual ao preço da compra + 10%.
    - Se o preço da compra for menor que a mediana da região+sazonalidade:<br/>
      O preço da venda será igual ao preço da compra + 30%.


2.5. Construção do dashboard

2.5.1. Tabelas
- Inserir as tabelas de compra e venda desenvolvidas anteriormente no dashboard;
- Calcular o preço médio dos imóveis de cada tabela;
- Criar tabela de estatísticas descritivas para os imóveis de compra e venda.

2.5.2. Mapas
- Criar mapa com a densidade de portfólio;
- Criar mapa com a densidade de preços;
- Criar mapa com a densidade do faturamento de cada imóvel, no dashboard de vendas.

2.5.3. Gráficos
- Atributos comerciais:
    - Evolução dos preços ano a ano;
    - Evolução dos preços dia a dia;
    - Histograma de preços.
    
- Atributos físicos:
    - Distribuição de número de quartos;
    - Distribuição de número de banheiros;
    - Distribuição de número andares;
    - Distribuição de vista para a costa.

<strong>3. Carregamento dos dados (Loading)</strong>

3.1. Validação de hipóteses

- <strong>H1</strong>: Imóveis que possuem vista para água são em média 30% mais caros;
- <strong>H2</strong>: Imóveis com data de construção menor que 1957 são em média 50% mais baratos;
- <strong>H3</strong>: Imóveis sem porão possuem em média área total 40% maior;
- <strong>H4</strong>: O crescimento do preço dos imóveis Year over Year (YoY) é de 10%;
- <strong>H5</strong>: Imóveis com 3 banheiros têm um crescimento Month over Month (MoM) de 15%;
- <strong>H6</strong>: Imóveis com reformas são em média 20% mais caros;
- <strong>H7</strong>: Imóveis com condição 3 são em média 40% mais caros que os imóveis com condição 1;
- <strong>H8</strong>: Imóveis com até 2 quartos são em média 10% mais baratos ;
- <strong>H9</strong>: Imóveis com porão são em média 5% mais caros;
- <strong>H10</strong>: Imóveis são vendidos no verão por um preço médio 15% maior que no inverno.

3.2. Avaliação de insights para o negócio

#### Entrada
- Os dados deste projeto foram retirados do portal Kaggle e estão disponíveis no link:
    
    [https://www.kaggle.com/datasets/harlfoxem/housesalesprediction](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)



## 4. Teste de hipóteses e insights do negócio

### 4.1. Hipóteses
<p align="justify"> Foram testadas 10 hipóteses acerca do conjunto de dados dos imóveis, com seus resultados e descrições abaixo:</p>

| Hipótese | Validação | Significado para o negócio |
|:---------|:----------|:---------------------------|
| <strong>H1: </strong>Imóveis com porão possuem em média área total 20% maior | Verdadeira | A média de área total construída dos imóveis com porão é 20,13% maior que aqueles que não possuem este cômodo. Devem ser considerados visto que o aumento de área total é significativo. |
| <strong>H2: </strong>Imóveis com reformas são em média 40% mais caros | Verdadeira | O preço médio dos imóveis que foram reformados é 43% em relação aos que nunca passaram por processos de renovação. É aconselhável comprar imóveis com condições boas para então reformá-los visando lucro na revenda. |
| <strong>H3: </strong>Imóveis com até 2 quartos são em média 30% mais baratos. | Verdadeira | Os imóveis com menos de 2 quartos são em média 30% mais baratos que aqueles que possuem mais dormitórios. Estes imóveis são boa opção de portfólio com preços mais baixos. |
| <strong>H4: </strong>Imóveis que possuem vista para água são em média 30% mais caros | Falsa | Imóveis com vista para a água são em média 214% mais caros. |
| <strong>H5: </strong>Imóveis com data de construção menor que 1957 são em média 50% mais baratos | Falsa | Os imóveis mais antigos possuem pequena variação de preço médio comparado aos mais novos, construídos a partir de 1957, sendo apenas 2.83% mais barato. Quando comparado com outros atributos do portfólio, este possui menor significância. |
| <strong>H6: </strong>O crescimento do preço dos imóveis Year over Year (YoY) é de 10% | Falsa | O preço médio dos imóveis vendidos em 2015 são apenas 0.53% maiores que aqueles vendidos no ano anterior. Assim, este comportamento não deve ser levado em conta no estudo. |
| <strong>H7: </strong>O crescimento do preço dos imóveis Month over Month (MoM) de 15% | Falsa | Entre os meses de maio/2014 e maio/2015, a variação do preço médio dos imóveis variou dentro de um intervalo de -3% e 7% em relação ao mês anterior, nunca alcançando uma variação de 15%. |
| <strong>H8: </strong>Imóveis com condição a partir de 3 são em média 40% mais caros que os imóveis com condição 1. | Falsa | Imóveis com condições acima de 3, ou seja, os imóveis que são considerados "bons" ou melhores, possuem preço médio 60% maiores que aqueles com condições ruins. Portanto, estes imóveis possuem maior valor de mercado. |
| <strong>H9: </strong>Imóveis com porão são em média 5% mais caros. | Falsa | Imóveis com porão, além de maiores em área total, são também 28% mais caros. Consequentemente, são imóveis mais bem avaliados. |
| <strong>H10: </strong>Imóveis são vendidos no verão por um preço médio 15% maior que no inverno. | Falsa | A variação entre os preços médios dos imóveis vendidos no verão e no inverno é de apenas 3%. Ou seja, não há variação significativa entre os preços nas duas estações. |


### 4.2. Insights
<p align="justify" >A análise exploratória dos dados das propriedades disponíveis para compra e revenda pela House Rocket proporciona alguns insights:</p>

#### Insight 1: Imóveis com vista para a água
<p align="justify" >O valor de mercado dos imóveis é fortemente influenciado pela sua localização, principalmente em relação à proximidade a grandes corpos d'água. Neste portfólio, as propriedades situadas à beira dos lagos presentes na região de Seattle, WA apresentam um preço médio 214% maior que aquelas situadas distante das costas.</p>

#### Insight 2: Imóveis que foram reformados
<p align="justify" ">Reformas elevam consideravelmente o preço dos imóveis do portfólio analisado. Comparadas àquelas que não passaram por nenhum processo de renovação, as propriedades reformadas possuem preço em média 40% maiores.</p>

#### Insight 3: Idade de construção dos imóveis
<p align="justify" >Foram analisadas as idades dos imóveis. A diferença entre o preço médio dos imóveis que foram constrídos antes e depois de 1957 (a mediana dos valores dos anos de contrução, que vão de 1900 a 2015) é de apenas 2.83%. Assim, esta variável não é significante comparada à influência dos outros atributos do conjunto de dados.</p>


## 5. Resultados financeiros para o negócio
<p align="justify">A partir das considerações sobre os imóveis, levando em conta as condições físicas, estação de compra e atributos físicos, são obtidos <strong>3872</strong> propriedades recomendadas para compra. As somas dos preços de compra e venda, além como o <strong>faturamento total</strong> possível estão descritos na tabela abaixo: </p>

| Número de imóveis | Preço de compra total | Preço de venda total | Faturamento total |
|:-----------------:|:---------------------:|:--------------------:|:-----------------:|
|       3872        | \$1.522.626.895,00    | \$1.959.734.476,70   | \$437.107.581,70  |

<p align="justify" >Evidentemente, devido à provável impossibilidade de adquirir todos os imóveis sugeridos imediatamente, devem ser levadas em conta fatores como localização, tamanho dos imóveis, recursos financeiros disponíveis e outros para diversificação do portfólio.</p>

## 6. Conclusão
<p align="justify" >Este documento provê uma análise exploratória de um conjunto de dados de imóveis disponíveis para a compra. Por meio de uma empresa fictícia com modelo de negócio bem definido, foi possível apresentar um processo completo de limpeza, carregamento e transformação de dados. O conjunto bruto foi explicado, foram propostas premissas sobre os dados e, assim, os imóveis foram categorizados em "Comprar" ou "Não comprar". Para ajudar o público final deste estudo na análise e visualização das propriedades, foram desenvolvidos dois dashboards com tabelas, mapas e gráficos. Por fim, este documento trouxe os resultados financeiros para o negócio, apresentando o faturamento máximo do portfólio de imóveis.</p>

## 7. Próximos passos
<p align="justify" >Este projeto pode ir além nas análises e visualizações já aqui desenvolvidas, incluindo intens como:</p>

>- Inclusão de banheiros considerados decimais (como 3/4 de banheiro sendo um lavatório que não possui chuveiro ou banheiro), que foram arredondados como premissa neste trabalho;<br/>
>- Refinamento do preço de venda dos imóveis, levando em conta não apenas o preço médio por região e a sazonalidade, mas também atributos físicos das propriedades;<br/>
>- Análise e sugestão de renovações nos imóveis para ampliação do portfólio da empresa.

## 8. Tecnologias
### Desenvolvimento do código
[<img src="https://upload.wikimedia.org/wikipedia/commons/3/38/Jupyter_logo.svg" style="height: 50px" align="left"/>](https://jupyter.org/)

[<img src="https://upload.wikimedia.org/wikipedia/commons/1/1d/PyCharm_Icon.svg" style="height: 50px" align="left"/>](https://www.jetbrains.com/pt-br/pycharm/)

[<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/1024px-Python.svg.png" style="height: 50px" align="left"/>](https://www.python.org/)
                                                                                                                  
[<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/1200px-Pandas_logo.svg.png" style="height: 50px" align="left"/>](https://pandas.pydata.org/)                                                                                                                                           
                                                                                                                                                  
[<img src="https://geopandas.org/en/latest/_images/geopandas_logo.png" style="height: 40px" align="left"/>](https://geopandas.org/en/stable/)<br/><br/><br/>

### Construção e publicação dos dashboards
[<img src="https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.svg" style="height: 50px" align="left"/>](https://streamlit.io/)<br/><br/>

                                                                                                                    
## 9. Sobre o autor
Olá! Meu nome é Lucas Rodrigues.<br/>
Conecte-se comigo no meu [Linkedin](https://www.linkedin.com/in/lucasrodrigues3/).
