# Zebrinha Azul

### Olá, sejam bem-vindos ao *data app* da **Zebrinha Azul**

Somos uma startup que busca trazer soluções de geolocalização para nossos clientes. Aqui, você poderá acompanhar a previsão do tempo atualizada de hora em hora, além de obter informações sobre as rotas de viagens mais populares dos nossos clientes. Estamos sempre expandindo e melhorando, então adoraríamos receber seu feedback :)

### Projeto

A Zebrinha Azul é uma combinação de duas soluções. A primeira é um aplicativo web construído em *Dash*, alimentado por um banco provisionado na *Redshift*. a arquitetura é baseada no modelo **pages** do Dash, utilizando o `use_pages` no arquivo `app.py`.

O **Dash** é uma framework da *Plotly* para construção de pequenos aplicativos web em puro **Python**. Trata-se de uma abstração em cima de *Flask* e *React*. Decidimos por essa ferramenta por facilitar o desenvolvimento rápido de produtos *reativos*.


##### Prós do Dash

- Rápido de desenvolver
- Altamente customizável
- Traduz a sintaxe de construção front-end para a linguagem python, respeitando estruturas clássicas de *html*.
- Integração natural com Plotly e Bootstrap

##### Contras do Dash

- Por ter alto nível de abstração, é dependente de estruturas mais definidas de código
- Essa estrutura não se dá bem com modularização, o que deixa os *scripts* muito grandes
- Deploy não é tão simples sem usar a versão paga


### Repositórios
- [Zebrinha Azul Data App](https://github.com/samurai-py/zebrinha-azul-dash-data-app)
- [ETL Zebrinha Azul com Astro](https://github.com/samurai-py/weather-traffic-etl)