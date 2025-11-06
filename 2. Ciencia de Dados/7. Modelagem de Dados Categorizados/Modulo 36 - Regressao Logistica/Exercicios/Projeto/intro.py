import streamlit as st

st.title("Ciências de Dados - EBAC")
st.header("Módulo 37 - Tarefa II: Credit Scoring")

st.write("Neste módulo, exploramos uma ferramenta essencial no mundo financeiro para avaliar o risco de inadimplência de clientes, ajudando instituições como bancos e fintechs a tomar decisões mais assertivas sobre concessão de crédito. Vamos começar com uma visão geral dos conceitos chave que guiarão nossa análise.")

st.subheader("O que é Credit Scoring (CS)?")
st.markdown("----------------------------------------------------------------------")
st.write("O Credit Scoring é um modelo estatístico utilizado para prever a probabilidade de um cliente não cumprir com suas obrigações de pagamento (inadimplência) com base em dados históricos e variáveis como histórico de crédito, renda, idade, tempo de emprego e comportamentos financeiros. Em essência, o CS atribui uma pontuação numérica a cada solicitante de crédito, onde pontuações mais altas indicam menor risco. Essa abordagem permite automatizar e padronizar avaliações, reduzindo vieses humanos e otimizando o processo de aprovação de empréstimos, cartões de crédito ou financiamentos. No nosso exercício, utilizaremos técnicas de análise de dados para construir e validar um modelo de CS simples, focando em precisão e interpretabilidade.")

st.subheader("O que são Safras (Vintages)?")
st.markdown("----------------------------------------------------------------------")
st.write("No contexto de credit scoring, as safras (ou vintages, em inglês) referem-se a coortes de empréstimos ou contratos de crédito originados em períodos específicos de tempo, como meses ou trimestres. Elas funcionam como 'colheitas' anuais ou sazonais de dados, permitindo que analisemos o desempenho de grupos homogêneos ao longo do tempo. Isso é crucial para capturar tendências sazonais, mudanças econômicas ou evoluções no portfólio de crédito.")

st.write("No nosso desenho amostral, adotaremos 15 safras, correspondendo a 15 meses consecutivos de originação de crédito (por exemplo, de janeiro de 2023 a março de 2024). Cada safra será tratada como uma unidade independente para treinamento e teste do modelo, garantindo que o CS seja robusto a variações temporais e evite overfitting a um único período.")

st.subheader("O que é Performance no Credit Scoring?")
st.markdown("----------------------------------------------------------------------")
st.write("A performance mede o comportamento real dos empréstimos após a concessão, focando em métricas como taxa de inadimplência (default rate), atrasos de pagamento ou recuperação de valores. Ela é observada ao longo de um horizonte temporal fixo, permitindo avaliar quão bem o modelo de CS prevê riscos reais.")
st.write("Neste exercício, utilizaremos 12 meses de performance para cada safra, ou seja, acompanharemos o status de cada contrato por um ano completo após sua originação. Isso nos dará uma visão madura do risco, capturando padrões de default que podem demorar a se manifestar (como em empréstimos de longo prazo). Métricas como a taxa de default cumulativa aos 12 meses serão centrais para validar a acurácia do modelo.")
