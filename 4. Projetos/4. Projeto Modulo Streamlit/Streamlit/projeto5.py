import streamlit as st

st.set_page_config(page_title="Projeto 5", page_icon="📊")

intro = st.Page("intro.py", title = "Etapa 1: Entedimento de Agrupamento")
dados = st.Page("dados.py", title = "Etapa 2: Entedimento dos Dados")
clean = st.Page("clean.py", title = "Etapa 3: Limpeza dos Dados")
kmeans = st.Page("kmeans.py", title = "Etapa 4: K-Means")
hierarquico = st.Page("hierarquico.py", title = "Etapa 5: Agrupamento Hierarquico")

st.navigation([intro, dados, clean, kmeans, hierarquico]).run()