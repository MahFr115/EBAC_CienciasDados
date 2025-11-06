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
st.header("Agrupamento dos Dados")

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

train["tempo_emprego"] = train["tempo_emprego"].fillna(train.groupby(["tipo_renda"])["tempo_emprego"].transform("mean"))
############################################################################################################
st.write("Para melhoria da análise e tratamento de outliers proponho o reagrupamento observado na análise biavariada dos dados como:")

st.write("Novos grupos de idade:")

st.code(''' 
idades = [
    "26-29.5",
    "30-35",
    "36-40",
    "41-46",
    "47-52",
    "53-54",
    "55-62",
    "64-65"
]
''', language = "python")

st.write("Novos grupos de tempo_emprego:")

st.code(''' 
tempo_emprego = [
    "0-1.9",
    "2-5.8",
    "6-7",
    "7.1-9.5",
    "11-25"
]
''', language = "python")

st.write("Novos grupos de renda:")

st.code(''' 
renda = [
    "0-1190", 
    "1190-1753", 
    "1753-2297", 
    "2297-2861", 
    "2861-3468", 
    "3468-4141", 
    "4141-4892", 
    "4892-5747", 
    "5747-6728",
    "6728-7862",
    "7862-9186",
    "9186-10793",
    "10793-18318",
    "18318-29748",
    "29748-4083986"
]
''', language = "python")

############################################################################################################
def biv_continua(var, df, ncat=None, bins=None, labels=None):
    df_local = df.copy()
    df_local['bom'] = 1 - df_local['mau']

    # Criar categoria
    if bins is not None:
        df_local['categoria'] = pd.cut(df_local[var], bins=bins, labels=labels, include_lowest=True)
    elif ncat is not None:
        df_local['categoria'], bins = pd.qcut(df_local[var], ncat, retbins=True, precision=0, duplicates='drop')
    else:
        raise ValueError("Você deve fornecer ncat ou bins.")

    g = df_local.groupby('categoria')

    biv = pd.DataFrame({
        'qt_bom': g['bom'].sum(),
        'qt_mau': g['mau'].sum(),
        'mau': g['mau'].mean(), 
        var: g[var].mean(), 
        'cont': g[var].count()
    })

    # Intervalos de confiança para mau
    biv['ep'] = (biv['mau'] * (1 - biv['mau']) / biv['cont']) ** 0.5
    biv['mau_sup'] = biv['mau'] + t.ppf(0.975, biv['cont'] - 1) * biv['ep']
    biv['mau_inf'] = biv['mau'] - t.ppf(0.975, biv['cont'] - 1) * biv['ep']

    tx_mau_geral = df_local['mau'].mean()
    woe_geral = np.log(tx_mau_geral / (1 - tx_mau_geral))

    # WOE e IV
    biv['logit'] = np.log(biv['mau'] / (1 - biv['mau']))
    biv['woe'] = biv['logit'] - woe_geral
    biv['iv_parcial'] = ((biv['qt_mau'] / df_local['mau'].sum()) -
                         (biv['qt_bom'] / df_local['bom'].sum())) * biv['woe']
    biv['IV_total'] = biv['iv_parcial'].sum()

    st.write(f"\n🔹 Variável: {var}")
    st.write(f"📊 IV total: {biv['IV_total'].iloc[0]:.5f}\n")
    st.table(biv[[var, 'qt_mau', 'qt_bom', 'mau', 'woe', 'iv_parcial']].reset_index(drop=True))

    # Gráficos
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].plot(biv[var], biv['woe'], ':bo', label='WOE', color = "violet")
    ax[0].set_ylabel("Weight of Evidence")
    ax[0].set_title(f"WOE de {var}")
    ax[0].legend()
    biv['cont'].plot.bar(ax=ax[1], color = "pink")
    ax[1].set_title("Frequência por categoria")
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write("-"*100)

    return biv

############################################################################################################

bins = [26, 29.5, 35, 40, 46, 52, 54, 62, 65]
labels = [
    "26-29.5",
    "30-35",
    "36-40",
    "41-46",
    "47-52",
    "53-54",
    "55-62",
    "64-65"
]

biv_continua("idade", df = df_, bins = bins, labels = labels)


bins_te = [0, 1.9, 5.8, 7.0, 9.5, 25]
labels_te = [
    "0-1.9",
    "2-5.8",
    "6-7",
    "7.1-9.5",
    "11-25"
]
biv_continua("tempo_emprego", df = df_, bins = bins_te, labels = labels_te)


bins_renda = [
    0,     
    1190,
    1753, 
    2297,
    2861, 
    3468, 
    4141, 
    4892, 
    5747, 
    6728, 
    7862, 
    9186, 
    10793,    
    18318,    
    29748,    
    4083986   
]

labels_renda = [
    "0-1190", 
    "1190-1753", 
    "1753-2297", 
    "2297-2861", 
    "2861-3468", 
    "3468-4141", 
    "4141-4892", 
    "4892-5747", 
    "5747-6728",
    "6728-7862",
    "7862-9186",
    "9186-10793",
    "10793-18318",
    "18318-29748",
    "29748-4083986"
]


biv_continua("renda", df = df_, bins = bins_renda, labels = labels_renda)