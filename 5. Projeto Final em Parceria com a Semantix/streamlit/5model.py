import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
import seaborn as sns

from phik.report import plot_correlation_matrix

import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from pycaret.regression import *

from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report 

import pickle 

df = pd.read_csv('../data/processed/base_modelo.csv')

cat = ['genero_cluster', 'tipo_dia', 'mes']
exp = setup(data = df, 
            target = 'lotacao',
            session_id = 42,
            normalize = True,           
            categorical_features = cat,  
            train_size = 0.8)

def treinar_modelos():
    best = compare_models(fold=10, sort="R2")
    df_best = pull()
    tuned = tune_model(best)
    df_tuned = pull()
    py_bst = finalize_model(tuned)
    plot_model(py_bst, plot="feature")
    df_feat = pull()
    return best, py_bst, df_best, df_tuned, df_feat

# Variável resposta
y = df['lotacao']
# Variaveis dependentes
X = df.drop(['lotacao'], axis = 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
train_df = X_train.copy()
train_df['lotacao'] = y_train
test_df = X_test.copy()
test_df['lotacao'] = y_test

formula_1 = '''
     lotacao ~ ano + C(genero_cluster) + I(popularidade**0.5) + C(tipo_dia) + C(mes) + distancia_dias_anterior
'''
md1 = smf.glm(formula_1, data=train_df, family=sm.families.Gaussian()).fit()  

formula_2 = '''
      lotacao ~  I(popularidade**2) + C(genero_cluster) + C(tipo_dia) * C(mes) * ano + distancia_dias_anterior
'''
md2= smf.glm(formula_2, data=train_df, family=sm.families.Gaussian()).fit()  

formula_3 = '''
      lotacao ~  I(popularidade**2) * C(genero_cluster) + C(tipo_dia) * C(mes) * ano + distancia_dias_anterior
'''
md3= smf.glm(formula_3, data=train_df, family=sm.families.Gaussian()).fit()  

formula_4= '''
      lotacao ~  I(popularidade**2) * C(genero_cluster) + C(tipo_dia) * C(mes) * ano + I(distancia_dias_anterior) * distancia_dias_anterior
'''
md4= smf.glm(formula_4, data=train_df, family=sm.families.Gaussian()).fit()  

formula_5 = '''
      lotacao ~ I(popularidade**2) * C(genero_cluster) + C(mes) * I(ano**2) +  I(distancia_dias_anterior) * distancia_dias_anterior
'''
md5= smf.glm(formula_5, data=train_df, family=sm.families.Gamma(link=sm.families.links.log())).fit()  

X_sample = df.drop(columns=['lotacao']).copy()
def bt_modelo(oque, modelo, base, formula, key_suffix):
    if oque == "modelo":
        label = "do Modelo Final"
        file_name = "modelo_final"
        data_bytes = pickle.dumps(modelo)

    elif oque == "colunas":
        label = "das Colunas do Modelo"
        file_name = "colunas_esperadas"
        data_bytes = pickle.dumps(base.columns.tolist())

    elif oque == "completo":
        label = "do Modelo Completo"
        file_name = "modelo_completo"
        data_bytes = pickle.dumps({
            "modelo": modelo,
            "colunas": base.columns.tolist(),
            "formula": formula
        })

    else:
        st.error("Tipo de download inválido")
        return

    st.download_button(
        label=f"⬇️ Download {label}",
        data=data_bytes,
        file_name=f"{file_name}.pkl",
        mime="application/octet-stream",
        key=f"download_{oque}_{key_suffix}"
    )
###############################################################################
st.title("🎶 Previsão de Demanda para Shows Musicais em São Paulo")

st.header("🎰 Desenvolvimento do Modelo")

st.write("""Para a etapa de modelagem, será adotada a base de dados desenvolvida 
no capítulo anterior 'Ralação entre Variáveis'.""")

st.dataframe(df.head())

prof = ProfileReport(df, title='Profiling Report da Base de Modelagem', minimal = True)
mostrar = st.toggle("📊 Mostrar Profiling Report")

if mostrar:
    st.components.v1.html(
        prof.to_html(),
        height=800,
        scrolling=True
    )

################################################################################
st.subheader("Downloads do Melhor Modelo")

col1, col2, col3 = st.columns(3)
with col1:
    bt_modelo("modelo", md5, train_df, formula_5, 'topo')
with col2:
    bt_modelo("colunas", md5, train_df, formula_5, 'topo')
with col3:
    bt_modelo("completo", md5, train_df, formula_5, 'topo')
###############################################################################
st.subheader("Utilizando o Pycaret")

best, py_bst, df_best, df_tuned, df_feat = treinar_modelos()

mostrar_modelagem = st.toggle("📊 Mostrar comparação e resultados dos modelos")

if mostrar_modelagem:

    st.markdown("#### Comparação dos Modelos")
    st.dataframe(df_best)

    st.markdown("#### Resultados do Modelo Tunado")
    st.dataframe(df_tuned)

    st.markdown("#### Importância das Variáveis")
    st.dataframe(df_feat)

st.dataframe(df_best.head(1))
###############################################################################
st.subheader("Modelagem Linear")
st.write("""Para separação dos dados de teste e treino, considerando as 1159 entradas, 
utilizarei para teste, aproximadamente, 20% de registros para teste.""")
st.code('''
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
''', language = 'python')
##################################################################################
st.write("""Com base nos padrões identificados anteriormente e nas relações observadas entre as variáveis,
foram definidos modelos de regressão para teste de hipóteses.""")

st.info("""O primeiro modelo especificado para avaliação foi:
  
lotacao ~ ano + C(genero_cluster) + I(popularidade**0.5) + C(tipo_dia) + C(mes) + distancia_dias_anterior
""")

mostrar_md1 = st.toggle("📊 Mostrar Resultado do Primeiro Modelo")

if mostrar_md1:
    st.write(md1.summary())

st.write("""Em comparação ao modelo de Random Forest 
selecionado pelo PyCaret, este modelo apresentou ganhos nos 
indicadores Pseudo-R² e R². Apesar da evolução observada, o 
processo de modelagem seguirá em busca de melhorias adicionais.
""")

################################################################################
st.info("""O segundo modelo testado foi: 

 lotacao ~  I(popularidade**2) + C(genero_cluster) + C(tipo_dia) * C(mes) * ano + distancia_dias_anterior""")
 
mostrar_md2 = st.toggle("📊 Mostrar Resultado do Segundo Modelo")

if mostrar_md2:
    st.write(md2.summary())

st.write("""Houve uma grande melhora no valor de Pseudo-R² e 
uma melhora no valor de R². A próxima etapa consiste em 
testar diferentes interações entre as variáveis, buscando 
aprimorar ainda mais o desempenho do modelo.""")
################################################################################
st.info("""O terceiro modelo testado foi:

 lotacao ~  I(popularidade**2) * C(genero_cluster) + C(tipo_dia) * C(mes) * ano + distancia_dias_anterior * distancia_dias_anterior
""") 
mostrar_md3 = st.toggle("📊 Mostrar Resultado do Terceiro Modelo")

if mostrar_md3:
    st.write(md3.summary())
################################################################################
st.info("""Já o quarto modelo testado foi:

lotacao ~  I(popularidade**2) * C(genero_cluster) + C(tipo_dia) * C(mes) * ano + I(distancia_dias_anterior) * distancia_dias_anterior
""")
mostrar_md4 = st.toggle("📊 Mostrar Resultado do Quarto Modelo")

if mostrar_md4:
    st.write(md4.summary())
################################################################################
st.info("""E o quinto modelo testado foi:

lotacao ~ I(popularidade**2) * C(genero_cluster) + C(mes) * I(ano**2) +  I(distancia_dias_anterior) * distancia_dias_anterior

Mas para esse resultado a base de dados utilizada foi a Gamma e não o Glaussiano como nas anteriores.  
""") 
mostrar_md5 = st.toggle("📊 Mostrar Resultado do Quinto Modelo(Melhor)")

if mostrar_md5:
    st.write(md5.summary())

pred_test = md5.predict(test_df)
pseudo_r2 = 1 - (md5.deviance / md5.null_deviance)
st.write("Pseudo R²: ", pseudo_r2)

st.write("""
Este último modelo está usando um conceito Gamma e não 
Gaussiano como os anteriores. Nessa base o Pseudo R² entre 
0,2 e 0,4 já tem boa aceitabilidade.

Houve uma melhora no valor de **Pseudo-R²** e 
também no **R²**. Entre todos os modelos testados, este foi o 
que apresentou o melhor desempenho.""")
################################################################################

st.subheader("Decisão de Modelo")

st.write("""Após a análise das métricas de desempenho (R², 
MAE, RMSE, entre outras), observou-se que o modelo que 
apresentou os melhores resultados foi o **quinto modelo 
desenvolvido e testado**, baseado em um **Modelo Linear 
Generalizado (GLM)**, com distribuição Gamma. 

Esse modelo foi finalizado com `finalize_model()` e incorpora 
todo o pipeline de pré-processamento (imputação, encoding, 
normalização).  

A seguir, você pode fazer o download do modelo treinado e da 
lista exata de variáveis que ele espera receber.
""")
################################################################################
st.subheader("Downloads do Melhor Modelo")

col4, col5, col6 = st.columns(3)
with col4:
    bt_modelo("modelo", md5, train_df, formula_5, 'inferior')

with col5:
    bt_modelo("colunas", md5, train_df, formula_5, 'inferior')

with col6:
    bt_modelo("completo", md5, train_df, formula_5, 'inferior')
