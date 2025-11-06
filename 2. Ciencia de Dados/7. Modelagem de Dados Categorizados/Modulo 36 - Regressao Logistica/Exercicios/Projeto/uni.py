import streamlit as st
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import seaborn as sns
import os

st.title("Ciências de Dados - EBAC")
st.header("Análise Descritiva Básica Univariada")


file_path = os.path.join(os.path.dirname(__file__), 'credit_scoring.ftr')
df = pd.read_feather(file_path)

oot = df[pd.to_datetime(df.data_ref) > pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
train = df[pd.to_datetime(df.data_ref) <= pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
############################################################################################################################
st.subheader("Descrição por mês")

st.write("Número de análises por mês")

# Contagem real
train_counts = train["data_ref"].value_counts().sort_index()
oot_counts = oot["data_ref"].value_counts().sort_index()

st.write("Distribuição de registros por mês — Base de estudo")
fig1, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=train_counts.index.strftime('%m-%Y'), y=train_counts.values, color="violet", ax=ax)
ax.set_xlabel("Mês de referência")
ax.set_ylabel("Quantidade de registros")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.write("Distribuição de registros por mês — Base Out of Time (OOT)")
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=oot_counts.index.strftime('%m-%Y'), y=oot_counts.values, color="pink", ax=ax)
ax.set_xlabel("Mês de referência")
ax.set_ylabel("Quantidade de registros")
st.pyplot(fig)

#############################################################################################################################
st.subheader("Descritiva por variável")

df_ = train.drop(["data_ref", "index"], axis = 1)

st.write("Criar uma tabela descritiva para cada variável com as seguintes atributos: variável, tipo de dado, tipo de variável, número de respostas unitárias, mínimo, máximo, média, moda e respostas menos comuns:")
des_uni = pd.DataFrame({
    "variavel": df_.columns,
    "dtype": df_.dtypes.astype(str),
    "nmissing": df_.isna().sum().values,
    "valores_unicos": df_.nunique().values
})

des_uni["tipo_var"] = des_uni["dtype"].apply(lambda x: "quantitativo" if any(t in x for t in ["float", "int"]) else "qualitativo")
des_uni["papel"] = des_uni["variavel"].apply(lambda x: "resposta" if x == "mau" else "covariavel")
des_uni["moda"] = des_uni["variavel"].apply(lambda v: df[v].mode().iloc[0] if not df[v].mode().empty else None)
des_uni["menos_comum"] = des_uni["variavel"].apply(lambda v: df[v].value_counts().idxmin() if df[v].nunique() > 0 else None)
des_uni["mínimo"] = des_uni["variavel"].apply(lambda v: round(df[v].min(), 2) if des_uni.loc[des_uni["variavel"] == v, "tipo_var"].item() == "quantitativo" else "-")
des_uni["máximo"] = des_uni["variavel"].apply(lambda v: round(df[v].max(), 2) if des_uni.loc[des_uni["variavel"] == v, "tipo_var"].item() == "quantitativo" else "-")
des_uni["média"] = des_uni["variavel"].apply(lambda v: round(df[v].mean(), 2) if des_uni.loc[des_uni["variavel"] == v, "tipo_var"].item() == "quantitativo" else "-")
des_uni = des_uni.drop(["variavel"], axis = 1)

st.write(des_uni)
st.write("Ao realizar a Análise Exploratória de Dados (EDA), identificamos as seguintes características principais no dataset de Credit Scoring:")
st.markdown("* Valores Ausentes (Missing Values): Os missing values estão concentrados exclusivamente na variável tempo_emprego, representando uma oportunidade para tratamento como imputação por mediana ou remoção de registros, dependendo da estratégia de modelagem.")
st.markdown("* Variabilidade nas Variáveis Numéricas: Observa-se alta variabilidade tanto em tempo_emprego quanto em renda, com desvios-padrão elevados que indicam uma distribuição assimétrica e possivelmente a presença de outliers. Isso sugere a necessidade de transformações como logaritmo ou normalização para melhorar o desempenho de modelos preditivos.")
st.markdown("* Cardinalidade de Respostas Únicas: Essas duas variáveis se destacam pela grande quantidade de valores únicos em comparação às demais (categóricas, com baixa cardinalidade). Por exemplo, renda pode exibir milhares de valores distintos, o que reforça a recomendação de binning ou feature engineering para reduzir dimensionalidade e evitar overfitting.")
st.write("Essas observações preliminares guiarão as próximas etapas, como visualizações de distribuições e testes de correlação com a variável alvo mau")
#############################################################################################################################
