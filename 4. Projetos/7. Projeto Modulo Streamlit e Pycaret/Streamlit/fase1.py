import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

from matplotlib import pyplot as plt
from scipy.stats import t
from scipy.stats import ks_2samp

import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn import metrics
########################################################################
# Código 
df = pd.read_feather('credit_scoring.ftr')
oot = df[pd.to_datetime(df.data_ref) > pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
train = df[pd.to_datetime(df.data_ref) <= pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
train_counts = train["data_ref"].value_counts().sort_index()
oot_counts = oot["data_ref"].value_counts().sort_index()

df["tempo_emprego"] = df["tempo_emprego"].fillna(df.groupby(["tipo_renda"])["tempo_emprego"].transform("mean"))

train = df[pd.to_datetime(df.data_ref) <= pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
df_ = train.drop(["index", "data_ref"], axis = 1)
des_uni = pd.DataFrame({
    "variavel": df_.columns,
    "dtype": df_.dtypes.astype(str),
    "nmissing": df_.isna().sum().values,
    "valores_unicos": df_.nunique().values
})

fig1, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=train_counts.index.strftime('%m-%Y'), y=train_counts.values, color="violet", ax=ax)
ax.set_xlabel("Mês de referência")
ax.set_ylabel("Quantidade de registros")
plt.xticks(rotation=45)

fig2, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=oot_counts.index.strftime('%m-%Y'), y=oot_counts.values, color="pink", ax=ax)
ax.set_xlabel("Mês de referência")
ax.set_ylabel("Quantidade de registros")

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

formula = '''
    mau ~ I(idade**2) + I(-tempo_emprego) + I(1/renda) 
'''

rl = smf.glm(formula, data=train, family=sm.families.Binomial()).fit()

oot = df[pd.to_datetime(df.data_ref) > pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]

oot['score'] = rl.predict(oot)

# Acurácia
acc = metrics.accuracy_score(oot.mau, oot.score>.068)
#AUC
fpr, tpr, thresholds = metrics.roc_curve(oot.mau, oot.score)
auc = metrics.auc(fpr, tpr)
#Gini
gini = 2*auc -1
ks = ks_2samp(oot.loc[oot.mau == 1, 'score'], oot.loc[oot.mau != 1, 'score']).statistic


########################################################################

st.title("🐍 Estudo dos Dados")

st.markdown(''' ## Amostragem
Separe os três últimos meses como safras de validação out of time (oot).

Variáveis:
Considere que a variável data_ref não é uma variável explicativa, é somente uma variável indicadora da safra, e não deve ser utilizada na modelagem. A variávei index é um identificador do cliente, e também não deve ser utilizada como covariável (variável explicativa). As restantes podem ser utilizadas para prever a inadimplência, incluindo a renda.

Para separação da amostragem o código que se segue foi utilizado
''')

st.code('''
oot = df[pd.to_datetime(df.data_ref) > pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
train = df[pd.to_datetime(df.data_ref) <= pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
''', language = "python")

st.write("Datas presentes na base de desenvolvimento do modelo: ", train["data_ref"].unique())
st.write("Datas presentes na base de validação (out of time) do modelo: ", oot["data_ref"].unique())

st.markdown('''---
## Análise Descritiva Básica Univariada
* Descreva a base quanto ao número de linhas, número de linhas para cada mês em data_ref.
* Faça uma descritiva básica univariada de cada variável. Considere as naturezas diferentes: qualitativas e quantitativas.

Número de Análise por Mês - Distribuição de registros por mês — Base de estudo
''')
st.pyplot(fig1)

st.markdown('''Número de Análise por Mês - Distribuição de registros por mês — Base Out of Time (OOT)
''')
st.pyplot(fig2)

st.markdown('''Para desenvolvimento da análise descritiva de cada variável utilizei o seguinte código que gerou o seguinte recultado em tabela
''')

st.code('''df_ = train.drop(["index", "data_ref"], axis = 1)

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
''', language = "python")

st.write(des_uni)


st.write('''A primeira observação notada é que há missing valores apenas entre os dados de tempo_emprego. Notamos que há uma grande variabilidade entre os dados coletados de tempo_emprego e renda. E uma grande quantidade, se destacando em relação às outras, de respostas únicas para essas mesmas variáveis.''')
st.markdown('''---
## Análise Descritiva Bivariada

Para essa análise utilizei o seguinte código, com o resultado apresentado:
''')
st.code('''def IV(variavel, resposta):
    tab = pd.crosstab(variavel, resposta, margins=True, margins_name='total')

    rótulo_evento = tab.columns[0]
    rótulo_nao_evento = tab.columns[1]

    tab['pct_evento'] = tab[rótulo_evento]/tab.loc['total',rótulo_evento]
    tab['ep'] = tab[rótulo_evento]/tab.loc['total',rótulo_evento]
    
    tab['pct_nao_evento'] = tab[rótulo_nao_evento]/tab.loc['total',rótulo_nao_evento]
    tab['woe'] = np.log(tab.pct_evento/tab.pct_nao_evento)
    tab['iv_parcial'] = (tab.pct_evento - tab.pct_nao_evento)*tab.woe
    return tab['woe'].sum(), tab['iv_parcial'].sum()

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
''', language = "python")

st.write(des_uni)

st.markdown('''Sabemos que variáveis com IV inferior a 0,02 possuem poder preditivo praticamente nulo. Portanto, elas serão desconsideradas nas próximas etapas da análise. São elas:

* sexo
* posse_de_veiculo
* posse_de_imovel
* qtd_filhos
* tipo_renda
* educacao
* estad_civil
* tipo_residencia

Além disso, observa-se que a variável qt_pessoas_residencia apresentou IV = inf, o que indica separação perfeita entre as classes — ou seja, há categorias que ocorrem exclusivamente em um dos grupos (“bom” ou “mau”). Esse comportamento pode sinalizar problemas de representatividade ou inconsistência nos dados, e por isso a variável deve ser reavaliada, possivelmente por meio de reagrupamento de categorias ou tratamento de outliers.

Observa-se, também, que a variável renda apresenta um IV muito elevado, o que pode indicar risco de sobreajuste (overfitting) ou forte correlação com a variável resposta.

Contudo, considerando que o estudo tem como objetivo analisar a inadimplência de indivíduos, faz sentido manter a variável para avaliação, visto que ela é conceitualmente relevante para o contexto da análise.
''')

des_uni = des_uni.loc[des_uni.index.isin(["idade", "tempo_emprego", "renda", "qt_pessoas_residencia", "mau", "bom"])]
st.write(des_uni)

#########################################################################################################
st.markdown('''
### Análise Gráfica dos Dados
Pra análise gráfica de distribuição dos dados estudados utilizarei os seguintes códigos
Para variáveis discretas:''') 
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

##########################################################################################################
st.markdown('''
## Desenvolvimento do Modelo

Desenvolva um modelo de credit scoring através de uma regressão logística.
* Trate valores missings e outliers
* Trate 'zeros estruturais'
* Faça agrupamentos de categorias conforme vimos em aula
* Proponha uma equação preditiva para 'mau'
* Caso hajam categorias não significantes, justifique

Para tratamento dos dados faltantes de tempo_emprego substituirei os valores pela média por tipo de renda, utilizando o código:''')

st.code('''df["tempo_emprego"] = df["tempo_emprego"].fillna(df.groupby(["tipo_renda"])["tempo_emprego"].transform("mean"))
''', language = "python")

st.write("Também podemos notra após observação da etapa anterior a exclusão de variáveis de baixa relevância realizada na etapa anterior — baseada na análise de Information Value (IV), uma métrica chave para identificar o poder preditivo de cada feature em relação à inadimplência —, não restaram dados discretos (categóricos) na base de dados.")

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

############################################################################################################
st.write("Equação preditiva proposta")
st.write("Primeiro analisarei uma fórmula simples")
st.code('''
formula = 
    mau ~ idade + tempo_emprego  + renda + qt_pessoas_residencia


rl = smf.glm(formula, data=df_, family=sm.families.Binomial()).fit()
''', language = "python")

formula = '''
    mau ~ idade + tempo_emprego  + renda + qt_pessoas_residencia
'''

rl = smf.glm(formula, data=train, family=sm.families.Binomial()).fit()

st.write(rl.summary())
############################################################################################################
st.write("Pelos gráficos observados anteriormente percebmos que idade tem uma forma semalhante a uma equação concava de 2º grau, tempo_emprego uma equação inversa linear, qt_emprego_residencia convexa de 2º grau e em relação a renda uma hibérbole positiva")
st.code('''
formula = 
    mau ~ I(idade**2) + tempo_emprego + I(1/renda) + I(qt_pessoas_residencia**2)
''', language = "python")

formula = '''
    mau ~ I(idade**2) + tempo_emprego + I(1/renda) + I(qt_pessoas_residencia**2)
'''

rl = smf.glm(formula, data=train, family=sm.families.Binomial()).fit()

st.write(rl.summary())
############################################################################################################
st.write("Considerando os valores dos primeiros modelos excluirei da fórmula qt_pessoas_residencia por ter valor de p muito alto em ambas os resultados")
st.code('''
formula = 
    mau ~ I(idade**2) + I(-tempo_emprego) + I(1/renda) 
''', language = "python")

formula = '''
    mau ~ I(idade**2) + I(-tempo_emprego) + I(1/renda) 
'''

rl = smf.glm(formula, data=train, family=sm.families.Binomial()).fit()

st.write(rl.summary())
############################################################################################################

st.write("Foram testados trÊs modelos de regressão logística com o objetivo de avaliar o impacto das variáveis idade, tempo de emprego, renda e quantidade de pessoas na residência sobre a probabilidade de inadimplência. O primeiro modelo considerou as variáveis em sua forma original, enquanto o segundo aplicou transformações não lineares (idade², 1/renda e qt_pessoas_residencia²), visando capturar relações mais complexas entre os preditores e a variável resposta.")

st.write("Os segundo modelo apresentou melhor ajuste estatístico, com redução na deviance (de 2.4985e+05 para 2.4951e+05) e aumento do Pseudo R² de 0.04246 para 0.04301, indicando leve melhora na explicação da variância da resposta. Além disso, as variáveis transformadas (idade², tempo_emprego e 1/renda) mostraram-se altamente significativas (p < 0.001), sugerindo que essas relações não lineares descrevem melhor o comportamento dos dados.")

st.write("Por outro lado, a variável qt_pessoas_residencia, mesmo após a transformação quadrática, não apresentou significância estatística (p = 0.162) e seu impacto sobre o ajuste do modelo foi nulo. A exclusão dessa variável resultou em um modelo final mais parcimonioso, mantendo o mesmo nível de ajuste (Pseudo R² = 0.04301) e a mesma log-verossimilhança, mas com menor complexidade.")

st.write("Em síntese, o modelo final — composto por idade², tempo de emprego e renda (1/renda) — mostrou-se estatisticamente robusto, coerente com a teoria e mais eficiente, representando a melhor alternativa entre os testados. A relação entre as variáveis e a inadimplência manteve-se economicamente plausível: quanto maior a renda e o tempo de emprego, menor a probabilidade de inadimplência, enquanto a idade apresentou uma relação não linear, sugerindo que o risco é maior em faixas etárias intermediárias.")


#############################################
st.markdown('''
## Avaliação do Modelo
Avaliando o poder discriminante do modelo pelo menos avaliando acurácia, KS e Gini. Utiizando essas métricas nas bases de desenvolvimento e out of time. Análise realizado com o código:''')

st.code('''oot['score'] = rl.predict(oot)

# Acurácia
acc = metrics.accuracy_score(oot.mau, oot.score>.068)
#AUC
fpr, tpr, thresholds = metrics.roc_curve(oot.mau, oot.score)
auc = metrics.auc(fpr, tpr)
#Gini
gini = 2*auc -1
ks = ks_2samp(oot.loc[oot.mau == 1, 'score'], oot.loc[oot.mau != 1, 'score']).statistic

print('Acurácia: {0:.1%} \nAUC: {1:.1%} \nGINI: {2:.1%}\nKS: {3:.1%}'
      .format(acc, auc, gini, ks))
''', language = "python")

st.write("Acurácia: {0:.1%}".format(acc)) 
st.write("AUC: {0:.1%}".format(auc))
st.write("GINI: {0:.1%}".format(gini))
st.write("KS: {0:.1%}".format(ks))


st.write("Apesar da consistência estatística, as métricas de desempenho preditivo indicam baixa capacidade discriminatória. O modelo final apresentou acurácia de 14,5%, AUC de 26,7% e índice de Gini negativo (-46,6%), sugerindo que o modelo está classificando de forma inversa em relação à realidade observada. O KS (Kolmogorov–Smirnov) de 33,8% demonstra alguma separação entre bons e maus pagadores, porém ainda insuficiente para caracterizar um bom poder preditivo.")

st.write("Esses resultados indicam que, embora o modelo esteja estatisticamente ajustado e teoricamente coerente, sua performance preditiva é insatisfatória, demandando ajustes adicionais — como revisão de variáveis explicativas, novos tratamentos de outliers ou o uso de técnicas não lineares mais robustas (como árvores de decisão ou modelos de ensemble) para capturar padrões mais complexos nos dados.")
