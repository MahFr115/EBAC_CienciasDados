import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.feature_selection import mutual_info_regression
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

from ydata_profiling import ProfileReport
from tqdm import tqdm
from IPython.display import display, HTML

import streamlit as st
from streamlit_pandas_profiling import st_profile_report
import os

st.title("Projeto 2 - Previsão de Rendas")
st.header("EBAC: Profissão Ciências de Dados")

st.subheader("📊 Base de dados primária")
renda = pd.read_csv('./input/previsao_de_renda.csv')
st.dataframe(renda.head())

st.subheader("📊 Entendimento dos dados")

dados = {
    "Variável": [
        "data_ref", "id_cliente", "sexo", "posse_de_veiculo", "posse_de_imovel",
        "qtd_filhos", "tipo_renda", "educacao", "estado_civil", "tipo_residencia",
        "idade", "tempo_emprego", "qt_pessoas_residencia", "renda"
    ],
    "Descrição": [
        "Data de referência de coleta das variáveis", "Código de identificação do cliente",
        "Sexo do cliente", "Indica se o cliente possui veículo", "Indica se o cliente possui imóvel",
        "Quantidade de filhos do cliente", "Tipo de renda do cliente", "Grau de instrução do cliente",
        "Estado civil do cliente", "Tipo de residência do cliente (própria, alugada, etc)",
        "Idade do cliente", "Tempo no emprego atual",
        "Quantidade de pessoas que moram na residência", "Renda em reais"
    ],
    "Tipo": [
        "object", "int64", "object", "bool", "bool", "int64", "object", "object",
        "object", "object", "int64", "float64", "float64", "float64"
    ]
}

st.subheader("Criando o DataFrame")
df = pd.DataFrame(dados)

st.dataframe(df, use_container_width=True)

st.markdown("----------")

st.subheader("📊 Entendimento dos dados - Univariada")
prof = ProfileReport(renda, explorative=True, minimal=True)
st_profile_report(prof)

st.markdown("----------")

st.subheader("📊 Entendimento dos dados - Bivariadas")

st.subheader("Criação de heatmap para análise de relação entre variáveis")

plt.figure(figsize=(10,6))
sns.heatmap(renda.corr(numeric_only=True), annot=True, cmap='crest', fmt=".2f")
plt.title("Matriz de Correlação")
st.pyplot(plt)

st.text("""O gráfico anterior apresenta a relação entre múltiplas variáveis. Quanto maior a correlação entre elas, mais próximo de 1 será o valor, e mais intenso será o tom vermelho no fundo dos quadros que representam essa correlação.
Ao analisar esse gráfico, percebemos que as variáveis com as correlações mais fortes são:
qtd_filhos x qtd_pessoas_residencia;
tempo_emprego x renda e
idade x tempo_emprego.""")


st.subheader("Variação das variáveis no período")

fig, ax = plt.subplots(8,1,figsize=(10,70))
renda[['posse_de_imovel','renda']].plot(kind='hist', ax=ax[0], color = "#60ac94")
sns.lineplot(x='data_ref',y='renda', hue='posse_de_imovel',data=renda, ax=ax[1])
ax[1].tick_params(axis='x', rotation=45)
sns.lineplot(x='data_ref',y='renda', hue='posse_de_veiculo',data=renda, ax=ax[2])
ax[2].tick_params(axis='x', rotation=45)
sns.lineplot(x='data_ref',y='renda', hue='qtd_filhos',data=renda, ax=ax[3])
ax[3].tick_params(axis='x', rotation=45)
sns.lineplot(x='data_ref',y='renda', hue='tipo_renda',data=renda, ax=ax[4])
ax[4].tick_params(axis='x', rotation=45)
sns.lineplot(x='data_ref',y='renda', hue='educacao',data=renda, ax=ax[5])
ax[5].tick_params(axis='x', rotation=45)
sns.lineplot(x='data_ref',y='renda', hue='estado_civil',data=renda, ax=ax[6])
ax[6].tick_params(axis='x', rotation=45)
sns.lineplot(x='data_ref',y='renda', hue='tipo_residencia',data=renda, ax=ax[7])
ax[7].tick_params(axis='x', rotation=45)
sns.despine()
st.pyplot(plt)

st.text("""Nota-se que em relação ao período de data de referência há periodicidade na variação dos resultado encontrados.""")


st.subheader("Variação das variáveis em relação à renda")
fig, ax = plt.subplots(7,1,figsize=(10,50))
sns.barplot(x='posse_de_imovel',y='renda',data=renda, ax=ax[0], color = "#60ac94")
sns.barplot(x='posse_de_veiculo',y='renda',data=renda, ax=ax[1], color = "#60ac94")
sns.barplot(x='qtd_filhos',y='renda',data=renda, ax=ax[2], color = "#60ac94")
sns.barplot(x='tipo_renda',y='renda',data=renda, ax=ax[3], color = "#60ac94")
sns.barplot(x='educacao',y='renda',data=renda, ax=ax[4], color = "#60ac94")
sns.barplot(x='estado_civil',y='renda',data=renda, ax=ax[5], color = "#60ac94")
sns.barplot(x='tipo_residencia',y='renda',data=renda, ax=ax[6], color = "#60ac94")
sns.despine()
st.pyplot(plt)

st.text("""Nos gráficos apresentados anteriormente, percebemos uma maior variação dos dados de renda em relação ao tipo_renda, educação e qtd_filhos.""")
