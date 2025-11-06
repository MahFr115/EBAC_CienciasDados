import streamlit as st

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from scipy.stats import t
from scipy.stats import ks_2samp

import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn import metrics
import os

st.title("Ciências de Dados - EBAC")
st.header("Tratamento dos Dados")

file_path = os.path.join(os.path.dirname(__file__), 'credit_scoring.ftr')
df = pd.read_feather(file_path)

train = df[pd.to_datetime(df.data_ref) <= pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
df_ = train.drop(["index", "data_ref"], axis = 1)
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

##########################################################################################################
st.write("Para tratamento dos dados faltantes de tempo_emprego substituirei os valores pela média por tipo de renda, utilizando o código:")
st.code('''df["tempo_emprego"] = df["tempo_emprego"].fillna(df.groupby(["tipo_renda"])["tempo_emprego"].transform("mean"))
''', language = "python")
st.write("Também podemos notra após observação da etapa anterior a exclusão de variáveis de baixa relevância realizada na etapa anterior — baseada na análise de Information Value (IV), uma métrica chave para identificar o poder preditivo de cada feature em relação à inadimplência —, não restaram dados discretos (categóricos) na base de dados.")