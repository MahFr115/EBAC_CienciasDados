import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

st.title("Ciências de Dados - EBAC")
st.header("Limpeza da Base de Dados")

############################################################################################################
### Ler os arquivos

df = pd.read_csv("Projeto/online_shoppers_intention.csv")
##########################################################################################################

df.Revenue.value_counts(dropna=False)

st.write("Reduzirei as opções de respostas para \"VisitorType\" retirando as que tem valores \"Others\", uma vez que, como vimos, esses " \
"valores tem pouca expressão na base apresentada.")
st.write("Como são distribuidos os valores se há a categoria Others")
st.write(df[["VisitorType", "Revenue"]].value_counts())

st.write("-"*200)

st.write("Como são distribuidos os valores se não há a categoria Others")
df = df.drop(df[df["VisitorType"] == "Other"].index)
st.write(df[["VisitorType"]].value_counts())
st.write("-"*200)
##########################################################################################################

st.write("Nova Estrutura dos Dados:")
buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()
st.text(s)
st.write("-"*200)
##########################################################################################################

st.write("Heatmap para análise de relação entre variáveis")

plt.figure(figsize=(10,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de Correlação entre Variáveis")
st.pyplot(plt)

st.write("Considerando o desenho da matrizde correlação encontrada percebemos uma esperada e clara forte relação entre as variáveis já esperadas, " \
"sendo a relação entre \"BounceRates\" x \"ExitRates\" o de melhor correlação (0,91), seguindo do \"ProductRelated\" x \"ProductRelated_Duration\""
" (0,86), \"Informational\" x \"Informational_Duration\" (0,62) e \"Administrative\" x \"Administrative_Duration\" (0,6).")
st.write("Além desses percebemos uma boa relação entre \"PageValues\" x \"Revenue\" (0,49), sendo essa uma relação muito interessante, entre " \
"a média de páginas visitadas para um visitante fechar a compra.")
st.write("O \"Administrative\" x \"ProductRelated\" tem relação de 0,43, mostrando uma relação relativamente importante entre os visitantes de "
"páginas administrativas e de páginas de produtos.")