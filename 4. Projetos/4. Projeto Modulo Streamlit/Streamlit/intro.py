import streamlit as st

st.title("Ciências de Dados - EBAC")
st.header("Projeto: K-Means vs. Agrupamento Hierárquicos")

st.write("K-Means e Agrupamentos Hierárquicos são métodos de agrupamento utilizados no aprendizado de máquina não supervsionado, os " \
"pontos de dados não têm estrutura de classificação definida. Entretanto, ambos, se diferem em abordagens e resultados.")

st.subheader("K-Means")
st.markdown("----------------------------------------------------------------------")
st.write("Algoritmo interativo de clusterização, que agrupa os dados em relação à distância até o centroide objetivando a minimização " \
"da média dessa medida.")
st.image("https://miro.medium.com/v2/resize:fit:1200/0*_XwxbKHayTU8QG44.png")
st.write("Código em Python:")
st.code('''from sklearn.cluster import KMeans 
kmeans = KMeans(n_init = n, n_clusters = k, verbose = v)
kmeans.fit(X)''', language = "python")



st.subheader("Agrupamentos Hierárquicos")
st.markdown("----------------------------------------------------------------------")
st.write("Algoritmo que procura agrupar dados em uma estrutura de árvore de clusters aninhados. Identificando grupos de objetos semelhantes, " \
"organizados hierarquicamente, normalmente representados por Dendogramas.")
st.image("https://media.licdn.com/dms/image/v2/C4D12AQEDmtl1xFwrrw/article-inline_image-shrink_400_744/article-inline_image-shrink_400_744/0/1630270386504?e=2147483647&v=beta&t=ARfewrl88yV0hokPdoICfvhkxxBDgjRvBzMZiSEeyjQ")
st.write("Código em Python:")
st.code(''' from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from gower import gower_matrix

# Medidas       
distancia_gower = gower_matrix(df_g, cat_features=vars_cat)
gdv = squareform(distancia_gower,force='tovector')
Z = linkage(gdv, method='complete')

# Dendograma
dn = dendrogram(Z, truncate_mode='level',p=10,show_leaf_counts=True,ax=axs, color_threshold=.24)
        
# Análise
df_g['grupo3'] = fcluster(Z, 3 , criterion='maxclust')
''', language = "python")
