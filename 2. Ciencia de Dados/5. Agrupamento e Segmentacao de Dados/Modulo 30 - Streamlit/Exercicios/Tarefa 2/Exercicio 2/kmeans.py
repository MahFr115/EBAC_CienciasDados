import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from tqdm import tqdm

st.title("Ciências de Dados - EBAC")
st.header("K-Means")

df = pd.read_csv("online_shoppers_intention.csv")
df = df.drop(df[df["VisitorType"] == "Other"].index)
##########################################################################################################

st.write("Alteração da base de dados para o uso em clusterização:")

df["VisitorType"] = (df["VisitorType"] == "New_Visitor")
df.rename(columns={"VisitorType": "New_Visitor"}, inplace=True)
mapa_meses = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "June": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

df["Month"] = df["Month"].map(mapa_meses)

st.code('''df["VisitorType"] = (df["VisitorType"] == "New_Visitor")
df.rename(columns={"VisitorType": "New_Visitor"}, inplace=True)
mapa_meses = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "June": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}
df["Month"] = df["Month"].map(mapa_meses)''', language = "python")

##########################################################################################################
st.dataframe(df.head(10))
###########################################################################################################
st.write("Reduzindo o número de variáveis em df, considerando o resultado da matriz de correlação anterios. Utilizarei a quantidade de acessos " \
"no lugardo tempo uma vez que entendo que essa é mais importante, uma vez que uma pessoa pode acessar uma página e simplesmente esquecê-la " \
"perdida nas abas abertas.")
st.write("Colunas que permanecerão: \"Administrative\", \"Informational\", \"ProductRelated\", \"BounceRates\", \"PageValues\",	\"SpecialDay\", \"Month\", " \
"\"OperatingSystems\",\"Browser\", \"Region\", \"TrafficType\", \"New_Visitor\", \"Weekend\", \"Revenue\"")
df = df[["Administrative", "Informational", "ProductRelated", "BounceRates", "PageValues",	"SpecialDay", "Month", "OperatingSystems", "Browser", "Region", "TrafficType", "New_Visitor", "Weekend", "Revenue"]]

###############################################################################################################

sns.pairplot(df, hue="Revenue")

X = df.drop("Revenue", axis = 1)
y = df[["Revenue"]]

#####################################################################################################################
st.write("Gráfico de silhueta:")

y_cat = pd.Categorical.from_codes(codes=(y-1).values.flatten(), categories =["Revenue"])
y_cat.value_counts()

X_pad = pd.DataFrame(StandardScaler().fit_transform(X), columns = X.columns)
X_pad["y"] = y_cat

variaveis = X_pad.columns.drop("y")

# Inicializar uma lista vazia que vai conter os valores da silueta média
siluetas = []
# Este é o número máximo de grupos que vamos testar
max_clusters = 20

# O loop percorre de 2 até o máximo de clusters
for n_clusters in tqdm(range(2, max_clusters+1)):
    # k-means
    km = KMeans(n_clusters=n_clusters).fit(X_pad[variaveis])
    # Aqui calculamos a silueta e guardamos o resultado na lista "siluetas"
    siluetas.append(silhouette_score(X_pad[variaveis], km.labels_))
    # Essa lista define o nome dos grupos
    nomes_grupos = ["grupo_" + str(g) for g in range(n_clusters)]
    # Agora vamos adicionar uma coluna no dataframe X_pad com o agrupamento construido
    X_pad["grupos_"+str(n_clusters)] = pd.Categorical.from_codes(km.labels_, categories = nomes_grupos)


df_silueta = pd.DataFrame({"n_clusters": list(range(2, max_clusters+1)), "silueta_média": siluetas})

df_silueta.plot.line(x = "n_clusters", y = "silueta_média", marker="o", color="#00fa9a", figsize=(8,5))
plt.xticks(list(range(2, max_clusters+1)))
plt.grid(axis = "x")
st.pyplot(plt)

st.write("Melhores valores de clusteres: 5 > 2 > 6")
######################################################################################################
def kmeans(n):
    if n == 1:
        alg = "lloyd"
    else:
        alg = "elkan"
        
    kmeans = KMeans(n_clusters=n, max_iter=600, algorithm=alg)
    kmeans.fit(df)
    col = f"cluster_{n}"  
    df_copy = df.copy()  
    df_copy[col] = kmeans.labels_

    st.write(f"Análise Descritiva para {n} Clusters:")
    st.write(df_copy.groupby(col).mean())  
    st.write(df_copy[col].value_counts())
    
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(df_copy.drop(col, axis=1))
    pca1 = f"pca1_{n}"
    pca2 = f"pca2_{n}"
    
    df_copy[pca1] = X_pca[:, 0]
    df_copy[pca2] = X_pca[:, 1]
        
    fig, ax = plt.subplots(figsize=(10, 8))
    scatter = ax.scatter(df_copy[pca1], df_copy[pca2], c=df_copy[col], cmap="viridis", alpha=0.6)

    # Criar legenda dos clusters
    handles = []
    cmap = plt.cm.get_cmap("viridis")
    norm = plt.Normalize(vmin=0, vmax=n-1)
    for cluster_num in range(n):
        color = cmap(norm(cluster_num))
        handles.append(mpatches.Patch(color=color, label=f"Cluster {cluster_num}"))
    ax.legend(handles=handles, title="Clusters", loc="best")

    # Criar setas (variáveis projetadas nos componentes principais)
    coeff = pca.components_.T  # Corrigir a orientação
    scaling_factor = np.max(np.abs(X_pca)) * 0.1  # Escala para visualização

    for i in range(coeff.shape[0]):
        ax.arrow(0, 0, coeff[i,0]*scaling_factor, coeff[i,1]*scaling_factor,
                 color='r', alpha=0.7, head_width=0.2, head_length=0.2)
        ax.text(coeff[i,0]*scaling_factor*1.2, coeff[i,1]*scaling_factor*1.2,
                df.columns[i], color='k', ha='center', va='center', fontsize=8)

    ax.grid(True)
    plt.title(f'Clusters ({n}) - PCA Projection', fontsize=14)
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    st.pyplot(plt)

    if n == 1:
        return
    else:
        return df_copy, col
############################################################################################################    
kmeans(1)
st.write("Observando esse gráfico, plotado apenas para entendimento do desenho, podemos, visualmente separar os dados estudados em 3 grupos, o " \
"primeiro até, aproximadamente X = 25, em que há muitos pontos \"altos\" na curva. O segundo até aproximadamente X = 270, em que notamos, quase "
"uma linearidade decrescente nos dados extremos, com y máximo, salvo alguns \"outsiders\". E por último valores em que X é maior que 270, em " \
"que os dados se apresentam mais espaços. Considerando os dados obtidos anteriormente, faremos o estudo com 5, 2 e 6 clusters.")

df_5, col_5 = kmeans(5)
st.write("O resultado obtido com 5 clusters apresenta uma grande desigualdade na quantidade de valores divididos entre os grupos (8426 x 91), " \
"tornando a interpretação visual dos dados pouco clara, havendo uma sobreposição dos agrupamentos. Entretanto, há uma clara diferença entre " \
"os valores médios encontrados para ambos os clusteres, destacando-se os valores de ProductRelated e PageValues. Em relação aos valores de " \
"New_Visitor e Weekend, inicialmente classificados como booleans, podemos notar que para o primeiro há uma grande distinção entre seus valores, " \
"enquanto para o segundo não há grande variabilidade, mas eles continuam são persistentementes próximos de 0, ou seja podemos considerá-los " \
"como \"False\". Já em relação ao Revenue que segue a mesma caracterítica vemos uma grande variabilidade em seus valores, destacando-se o " \
"cluster 2 em que o valor é muito próximo de 0,8, podendo considerálo como \"True\".")
st.markdown('''Cluster 0: Menor Valor de Revenue
Cluster 1: Valores Médios
Cluster 2: Revenue True
Cluster 3: Muitas Visitas à Páginas Relacionadas a Produtos
Cluster 4: Valores Baixos''')

df_2, col_2 = kmeans(2)
st.write("O gráfico para 2 clusteres apresenta uma pior divisão visual, havendo mais sobreposição dos grupos, quando comparado ao de 5 clusters." \
" Entretanto, há uma menor diferença na separação dos dados, anteriormente sendo de 8426 para 91 (92x maior) e agora de 11246 para 999 (11x " \
"maior). Em relação ao estudo de variabilidade de variáveis, ele consitnua sendo similar ao apresnetao anteriormente, apesar de haver uma maior" \
" variaçãos dos resultados obtidos uma vez que há menos clusters a serem analisados. Também devemos considerar que não há um cluster de " \
"resultado mais positivo para Revenue nessa análise.")
st.markdown('''Cluster 0: Poucas Visitas à Páginas em Geral 
Cluster 1: Muitas Visitas à Quaisquer Páginas''')
st.write("-"*200)

st.write("Entre os valores observados anteriormente 5 clusters parece ter melhor resultado.")
st.write(df_5.groupby(col_5)[['BounceRates', 'Revenue']].mean())

############################################################################################################

st.subheader("Teste novas divisões de clusters, variando entre 2 e 20.")
n = st.number_input('Escolha um número:', min_value=2, max_value=20)

df_n, col_n = kmeans(n)

st.write(df_n.groupby(col_n)[['BounceRates', 'Revenue']].mean())