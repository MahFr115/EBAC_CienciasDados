🎵 Previsão de Público em Eventos Musicais
📌 Visão Geral

Este repositório contém um projeto de modelagem preditiva para estimativa de público em eventos musicais, utilizando técnicas de ciência de dados e aprendizado de máquina.
O objetivo é apoiar a tomada de decisão no planejamento de eventos, especialmente na escolha do local e no dimensionamento da estrutura, a partir de informações observáveis do artista, do evento e do contexto temporal.

O projeto contempla desde a análise exploratória dos dados até a implementação de um simulador interativo de público em Streamlit.
---
🧠 Problema de Negócio

A estimativa inadequada de público pode gerar:

Subdimensionamento ou superdimensionamento de espaços

Aumento de custos operacionais

Impactos negativos na experiência do público

Este projeto busca reduzir essas incertezas por meio de modelos preditivos baseados em dados históricos de eventos.
---
📊 Dados

O conjunto de dados contém informações históricas de eventos musicais, incluindo:

Variáveis do artista (ex.: gênero musical)

Variáveis do evento (ex.: tipo de dia, mês, evento/festival)

Variáveis do local (ex.: categoria do local)

Variável-alvo: público / lotação estimada

Durante o pré-processamento, variáveis redundantes relacionadas às características físicas do local foram removidas para reduzir multicolinearidade e simplificar o modelo.
---
🔍 Metodologia
1. Análise Exploratória de Dados (EDA)

Identificação de padrões sazonais

Avaliação de distribuições e outliers

Análise de correlação e redundância entre variáveis

2. Pré-processamento

Tratamento de variáveis categóricas

Normalização

Seleção de variáveis relevantes

3. Modelagem

Foram testados diferentes algoritmos de regressão, com destaque para:

Modelos baseados em árvores de decisão

Modelos estatísticos generalizados (GLM)

O GLM com distribuição Gamma apresentou o melhor desempenho global, considerando poder explicativo, estabilidade e métricas de avaliação.

4. Avaliação

Os modelos foram comparados utilizando métricas adequadas a problemas de regressão, permitindo avaliar desempenho preditivo e robustez.
---
🛠️ Aplicação em Produção

Como entrega prática, foi desenvolvido um simulador de público com interface interativa em Streamlit, permitindo:

Simulação de diferentes cenários de eventos

Estimativa do público esperado

Apoio à tomada de decisão operacional
---
📈 Principais Resultados

Modelos não lineares mostraram-se mais adequados para capturar interações complexas

O modelo final apresentou boa estabilidade e capacidade preditiva

A solução é facilmente adaptável para uso real com novos dados
---
🧪 Tecnologias Utilizadas

Python

Pandas, NumPy

Scikit-learn

PyCaret

Statsmodels

Streamlit

Matplotlib / Seaborn
---
📂 Estrutura do Repositório
├── data/               # Dados (ou instruções para obtenção)
├── notebooks/          # EDA e modelagem
├── models/             # Modelos treinados
├── app/                # Aplicação Streamlit
├── requirements.txt    # Dependências
└── README.md
---
🚀 Como Executar o Projeto

Clone o repositório:

git clone https://github.com/MahFr115/EBAC_CienciasDados.git
--- 
Instale as dependências:

pip install -r requirements.txt

Execute a aplicação Streamlit:

streamlit run app/app.py
---
📌 Próximos Passos

Inclusão de novas variáveis contextuais

Testes com modelos ensemble adicionais

Validação com dados externos

Deploy da aplicação em ambiente web
---
👤 Autora

Marina Pereira
Projeto desenvolvido para fins educacionais e analíticos em Ciência de Dados.