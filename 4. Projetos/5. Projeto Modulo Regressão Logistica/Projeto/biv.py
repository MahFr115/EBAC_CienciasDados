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
st.header("Análise Descritiva Bivariada")

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

st.write("Análise descritiva bivariada de cada variável")

st.write("Utilizaremos o seguinte código para cálculo do indice de variabilidade de cada variável")

st.code('''
def IV(variavel, resposta):
    tab = pd.crosstab(variavel, resposta, margins=True, margins_name='total')

    rótulo_evento = tab.columns[0]
    rótulo_nao_evento = tab.columns[1]

    tab['pct_evento'] = tab[rótulo_evento]/tab.loc['total',rótulo_evento]
    tab['ep'] = tab[rótulo_evento]/tab.loc['total',rótulo_evento]
    
    tab['pct_nao_evento'] = tab[rótulo_nao_evento]/tab.loc['total',rótulo_nao_evento]
    tab['woe'] = np.log(tab.pct_evento/tab.pct_nao_evento)
    tab['iv_parcial'] = (tab.pct_evento - tab.pct_nao_evento)*tab.woe
    return tab['woe'].sum(), tab['iv_parcial'].sum()
''', language = "python")

def IV(variavel, resposta):
    tab = pd.crosstab(variavel, resposta, margins=True, margins_name='total')

    rótulo_evento = tab.columns[0]
    rótulo_nao_evento = tab.columns[1]

    tab['pct_evento'] = tab[rótulo_evento]/tab.loc['total',rótulo_evento]
    tab['ep'] = tab[rótulo_evento]/tab.loc['total',rótulo_evento]
    
    tab['pct_nao_evento'] = tab[rótulo_nao_evento]/tab.loc['total',rótulo_nao_evento]
    tab['woe'] = np.log(tab.pct_evento/tab.pct_nao_evento)
    tab['iv_parcial'] = (tab.pct_evento - tab.pct_nao_evento)*tab.woe
    return tab['woe'].sum(), tab['iv_parcial'].sum()

st.write("Utilizando a tabela de dados calculada no item anterior (análise univariada), podemos calcular para as variáveis os dados de WOE e IV:")

for var in des_uni[des_uni.papel=="covariavel"].index:
    if  (des_uni.loc[var, "valores_unicos"]>15):
       woe, iv_total = IV(pd.qcut(df[var],q = 10,duplicates='drop'), df.mau)
    else: 
       woe, iv_total  = IV(df[var], df["mau"])
        
    des_uni.loc[var, "woe"] = woe
    des_uni.loc[var, "IV"] = iv_total

des_uni.loc["bom", "dtype"] = "bool"
des_uni.loc["bom", "tipo_var"] = "qualitativo"
des_uni.loc["bom", "papel"] = "resposta"

st.write(des_uni)


st.write("Sabemos que variáveis com IV inferior a 0,02 possuem poder preditivo praticamente nulo. Portanto, elas serão desconsideradas nas próximas etapas da análise. São elas:")
st.markdown("""
* sexo  
* posse_de_veiculo  
* posse_de_imovel  
* qtd_filhos  
* tipo_renda  
* educacao  
* estado_civil  
* tipo_residencia
""")
st.write("Além disso, observa-se que a variável qt_pessoas_residencia apresentou IV = inf, o que indica separação perfeita entre as classes — ou seja, há categorias que ocorrem exclusivamente em um dos grupos (“bom” ou “mau”). Esse comportamento pode sinalizar problemas de representatividade ou inconsistência nos dados, e por isso a variável deve ser reavaliada, possivelmente por meio de reagrupamento de categorias ou tratamento de outliers.")
st.write("Observa-se, também, que a variável renda apresenta um IV muito elevado, o que pode indicar risco de sobreajuste (overfitting) ou forte correlação com a variável resposta.")
st.write("Contudo, considerando que o estudo tem como objetivo analisar a inadimplência de indivíduos, faz sentido manter a variável para avaliação, visto que ela é conceitualmente relevante para o contexto da análise.")
#########################################################################################################
des_uni = des_uni.loc[des_uni.index.isin(["idade", "tempo_emprego", "renda", "qt_pessoas_residencia", "mau", "bom"])]
st.write(des_uni)

#########################################################################################################
st.subheader("Análise Gráfica dos Dados")
st.write("Pra análise gráfica de distribuição dos dados estudados utilizarei os seguintes códigos")
st.write("Para variáveis discretas:") 
st.code('''def biv_discreta(var, df):
    df['bom'] = 1 - df['mau']

    g = df.groupby(var)
    biv = pd.DataFrame({
        'qt_bom': g['bom'].sum(),
        'qt_mau': g['mau'].sum(),
        'mau': g['mau'].mean(),
        'cont': g[var].count()
    }).reset_index()

    # Intervalos de confiança
    biv['ep'] = (biv['mau'] * (1 - biv['mau']) / biv['cont']) ** 0.5
    biv['mau_sup'] = biv['mau'] + t.ppf(0.975, biv['cont'] - 1) * biv['ep']
    biv['mau_inf'] = biv['mau'] - t.ppf(0.975, biv['cont'] - 1) * biv['ep']

    tx_mau_geral = df['mau'].mean()
    woe_geral = np.log(tx_mau_geral / (1 - tx_mau_geral))

    biv['logit'] = np.log(biv['mau'] / (1 - biv['mau']))
    biv['woe'] = biv['logit'] - woe_geral

    biv['iv_parcial'] = ((biv['qt_mau'] / df['mau'].sum()) -
                         (biv['qt_bom'] / df['bom'].sum())) * biv['woe']
    biv['IV_total'] = biv['iv_parcial'].sum()

    print(f"\n🔹 Variável: {var}")
    print(f"📊 IV total: {biv['IV_total'].iloc[0]:.5f}\n")
    print(biv[[var, 'qt_mau', 'qt_bom', 'mau', 'woe', 'iv_parcial']].to_string(index=False))

    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].plot(biv[var], biv['woe'], ':bo', label='WOE')
    ax[0].set_ylabel("Weight of Evidence")
    ax[0].set_title(f"WOE de {var}")
    ax[0].legend()

    biv['cont'].plot.bar(ax=ax[1])
    ax[1].set_title("Frequência por categoria")

    plt.tight_layout()
    plt.show()

    return biv
''', language = "python")

#########################################################################################################
st.write("Para variáveis contínuas:")
st.code('''def biv_continua(var, df, ncat=None, bins=None, labels=None):
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

    print(f"\n🔹 Variável: {var}")
    print(f"📊 IV total: {biv['IV_total'].iloc[0]:.5f}\n")
    print(biv[[var, 'qt_mau', 'qt_bom', 'mau', 'woe', 'iv_parcial']].to_string(index=False))

    # Gráficos
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].plot(biv[var], biv['woe'], ':bo', label='WOE')
    ax[0].set_ylabel("Weight of Evidence")
    ax[0].set_title(f"WOE de {var}")
    ax[0].legend()
    biv['cont'].plot.bar(ax=ax[1])
    ax[1].set_title("Frequência por categoria")
    plt.tight_layout()
    plt.show()

    return biv
''', language = "python")
#########################################################################################################

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

#########################################################################################################

def biv_discreta(var, df):
    df['bom'] = 1 - df['mau']

    g = df.groupby(var)
    biv = pd.DataFrame({
        'qt_bom': g['bom'].sum(),
        'qt_mau': g['mau'].sum(),
        'mau': g['mau'].mean(),
        'cont': g[var].count()
    }).reset_index()

    # Intervalos de confiança
    biv['ep'] = (biv['mau'] * (1 - biv['mau']) / biv['cont']) ** 0.5
    biv['mau_sup'] = biv['mau'] + t.ppf(0.975, biv['cont'] - 1) * biv['ep']
    biv['mau_inf'] = biv['mau'] - t.ppf(0.975, biv['cont'] - 1) * biv['ep']

    tx_mau_geral = df['mau'].mean()
    woe_geral = np.log(tx_mau_geral / (1 - tx_mau_geral))

    biv['logit'] = np.log(biv['mau'] / (1 - biv['mau']))
    biv['woe'] = biv['logit'] - woe_geral

    biv['iv_parcial'] = ((biv['qt_mau'] / df['mau'].sum()) -
                         (biv['qt_bom'] / df['bom'].sum())) * biv['woe']
    biv['IV_total'] = biv['iv_parcial'].sum()

    print(f"\n🔹 Variável: {var}")
    print(f"📊 IV total: {biv['IV_total'].iloc[0]:.5f}\n")
    print(biv[[var, 'qt_mau', 'qt_bom', 'mau', 'woe', 'iv_parcial']].to_string(index=False))

    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].plot(biv[var], biv['woe'], ':bo', label='WOE')
    ax[0].set_ylabel("Weight of Evidence")
    ax[0].set_title(f"WOE de {var}")
    ax[0].legend()

    biv['cont'].plot.bar(ax=ax[1])
    ax[1].set_title("Frequência por categoria")

    plt.tight_layout()
    plt.show()

    return biv

#########################################################################################################
var = des_uni.index.unique()
var_sel = st.multiselect("Selecione a variável:", var, default=var)

# Filtrar DataFrame de acordo com seleção
df_filtrado = des_uni.loc[var_sel]
st.dataframe(df_filtrado)

# Separar variáveis qualitativas e quantitativas
qual_vars = df_filtrado[(df_filtrado['papel'] == "covariavel") & (df_filtrado['tipo_var'] == "qualitativo")].index
quant_vars = df_filtrado[(df_filtrado['papel'] == "covariavel") & (df_filtrado['tipo_var'] == "quantitativo")].index

# Processar variáveis qualitativas
for var_q in qual_vars:
    biv = biv_discreta(var_q, train) 

# Processar variáveis quantitativas
for var_qt in quant_vars:
    valores_unicos = des_uni.loc[var_qt, "valores_unicos"]
    
    if 16 < valores_unicos < 10001:
        gr = 15
    elif valores_unicos > 10000:
        gr = 20
    else:
        gr = valores_unicos

    gr = max(int(gr), 1)  # Garantir valor mínimo de 1
    biv_continua(var_qt, train, ncat=gr)  