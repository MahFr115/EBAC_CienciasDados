import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from gower import gower_matrix

from scipy.spatial.distance import pdist, squareform

st.title("Ciências de Dados - EBAC")
st.header("Agrupamento Hierarquico")


df = pd.read_csv('online_shoppers_intention.csv"')
df = df.drop(df[df["VisitorType"] == "Other"].index)
#############################################################################################################################

st.write("Reduzindo o número de variáveis em df, considerando o resultado da matriz de correlação anterios. Utilizarei a quantidade de acessos " \
"no lugardo tempo uma vez que entendo que essa é mais importante, uma vezque uma pessoa pode acessar uma página e simplesmente esquecê-la " \
"perdida nas abas abertas e por serem valores mais padronizados.")

st.write("Colunas que permanecerão: \"Administrative\", \"Informational\", \"ProductRelated\", \"BounceRates\", \"PageValues\",	\"SpecialDay\", \"Month\", " \
"\"OperatingSystems\",\"Browser\", \"Region\", \"TrafficType\", \"VisitorType\", \"Weekend\", \"Revenue\"")

df = df[["Administrative", "Informational", "ProductRelated", "BounceRates", "PageValues",	"SpecialDay", "Month", "OperatingSystems", "Browser", "Region", "TrafficType", "VisitorType", "Weekend", "Revenue"]]

st.write('Variáveis categóricas: "BouncesRates", "Revenue""')
st.write('Variáveis de datas: "SpecialDay", "Month", "Weekend"')
#############################################################################################################################

st.write("Divisão das bases X e y:")
st.code('''var = df.columns[df.columns != "Revenue"]
var_cat = var[-1]''', language = "python")
var = df.columns[df.columns != "Revenue"]
var_cat = var[-1]

st.write("Criando Dummies:")
st.code('''df_g = pd.get_dummies(df[var].dropna())
df_g.head()''', language = "python")
df_g = pd.get_dummies(df[var].dropna())
df_g.head()

st.write("Nome dascolunas depois de aplicar a dummies")
st.write(df_g.columns.values)

vars_cat = [True if x in {"Month_Aug", "Month_Dec", "Month_Feb", "Month_Jul", "Month_June", "Month_Mar", "Month_May", "Month_Nov", "Month_Oct", "Month_Sep", "VisitorType_New_Visitor", "VisitorType_Returning_Visitor"} else False for x in df_g.columns]

st.write("Distância do Centroide:")
st.code('''distancia_gower = gower_matrix(df_g, cat_features=vars_cat)
gdv = squareform(distancia_gower,force='tovector')
Z = linkage(gdv, method='complete')''', language = "python")

distancia_gower = gower_matrix(df_g, cat_features=vars_cat)
gdv = squareform(distancia_gower,force='tovector')
Z = linkage(gdv, method='complete')

st.write("Dendograma:")
fig,axs = plt.subplots(1,1,figsize=(12,12))
dn = dendrogram(Z, truncate_mode='level',p=10,show_leaf_counts=True,ax=axs, color_threshold=.24)
st.write(f"Leaves = {len(dn['leaves'])}")

st.write("Análise descitiva para 3 grupos:")
df_g['grupo3'] = fcluster(Z, 3 , criterion='maxclust')
st.write(df_g.grupo3.value_counts())

df_3 = df.reset_index().merge(df_g.reset_index(), how='left')
st.write(df_3.groupby(['VisitorType', 'Revenue','grupo3'])['index'].count().unstack().fillna(0).astype(int))

st.write("Análise descitiva para 4 grupos:")
df_g['grupo4'] = fcluster(Z, 4 , criterion='maxclust')
st.write(df_g.grupo4.value_counts())

df_4 = df.reset_index().merge(df_g.reset_index(), how='left')
st.write(df_4.groupby(['VisitorType', 'Revenue', 'grupo4'])['index'].count().unstack().fillna(0).astype(int))

st.write("Observando ambas as divisões em grupos estudadas (entre 3 e 4) percebemos que a divisão entre 4 grupos de dados parece mais homogênea.")
st.write("-"*200)

##############################################################################################################
st.subheader("Avaliação de resultados")
st.write("Para 4 clusters")
st.write(df_4.groupby('grupo4')[['BounceRates', 'Revenue']].mean())

st.write("Considerando os grupos criados a partir da segmentação em quatro partes, percebe-se uma melhor representação dos clientes-alvo no " \
"grupo 1. Como o objetivo do estudo é identificar grupos com maior Revenue e, ao mesmo tempo, com menores Bounce Rates, pode-se sugerir que o " \
"grupo 1 apresenta uma melhor compensação entre os indicadores analisados.")

##############################################################################################################
st.subheader("Teste novas divisões de agrupamentos.")
n = st.number_input('Escolha um número:', min_value=1)

grupo = f'grupo{n}'
df_g[grupo] = fcluster(Z, n , criterion='maxclust')
st.write(df_g[grupo].value_counts())

df_n = df.reset_index().merge(df_g.reset_index(), how='left')
st.write(df_n.groupby(['VisitorType', 'Revenue',grupo])['index'].count().unstack().fillna(0).astype(int))

st.write(df_n.groupby(grupo)[['BounceRates', 'Revenue']].mean())