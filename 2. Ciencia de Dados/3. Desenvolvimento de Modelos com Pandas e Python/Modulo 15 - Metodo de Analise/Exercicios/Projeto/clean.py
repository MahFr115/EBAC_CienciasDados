import pandas as pd
import numpy as np

import streamlit as st

import os

st.title("Projeto 2 - Previsão de Rendas")
st.header("EBAC: Profissão Ciências de Dados")
renda = pd.read_csv('./input/previsao_de_renda.csv')
st.subheader("🔡Seleção de Colunas")
st.dataframe(renda.head(1))
st.text("Retirando os dados que não interferem no valor de renda relativos. Os dados relativos ao período e ID dos clientes.")
renda = renda.drop(renda.columns[:3], axis = 1) 
st.dataframe(renda.head(1))

st.subheader("🧹Limpeza dos Dados")

st.text("A análise apresentada no passo \"Entendimento dos dados - Univariada\" mostra que apenas a variável tempo_emprego tem valores em branco.")
st.text("Para preencher esses valores faltosos de forma mais acertiva vou analisar quais os dados de tipo_renda esses valores acompanham.")

st.dataframe(renda[renda["tempo_emprego"].isna()].nunique())

st.text("Tabela com dados em branco:")
renda[renda["tempo_emprego"].isna()]

st.text("Preenchendo os valores do tempo de emprego em branco, com a média do valor em relação ao tipo de renda por idade ou, se não possível, pelo tipo de renda")

renda['tempo_emprego'] = renda['tempo_emprego'].fillna(
    renda.groupby(['idade', 'tipo_renda'])['tempo_emprego'].transform('mean')
)

renda['tempo_emprego'] = renda['tempo_emprego'].fillna(
    renda.groupby(['tipo_renda'])['tempo_emprego'].transform('mean')
)

st.text("Tabela limpa:")
renda[renda["tempo_emprego"].isna()]

st.subheader("⚒️Construindo novas variáveis")

code = """ 1. Tempo de emprego por idade (razão entre tempo_emprego e idade)
renda['tempo_emprego_por_idade'] = round(renda['tempo_emprego'] / renda['idade'], 2)

2. Renda per capta
renda['renda_per_capta'] = round(renda['renda']/ renda['qt_pessoas_residencia'], 2)

3. Renda por ano de emprego
renda['renda_por_tempo_emprego'] = round(renda['renda']/renda['tempo_emprego'], 2)"""

st.code(code)

renda['tempo_emprego_por_idade'] = round(renda['tempo_emprego'] / renda['idade'], 2)

renda['renda_per_capta'] = round(renda['renda']/ renda['qt_pessoas_residencia'], 2)

renda['renda_por_tempo_emprego'] = round(renda['renda']/renda['tempo_emprego'], 2)

st.dataframe(renda.head())

st.write(renda.info())

st.text("Os dados já estão em formatos úteis.")