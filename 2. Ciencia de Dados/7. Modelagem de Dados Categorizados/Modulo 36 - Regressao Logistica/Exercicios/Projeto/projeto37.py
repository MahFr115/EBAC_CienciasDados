import streamlit as st

st.set_page_config(page_title="Tarefa 2: Módulo 37", page_icon="📊")

intro = st.Page("intro.py", title = "Etapa 1: Entedimento de Credit Scoring")
dados = st.Page("dados.py", title = "Etapa 2: Entedimento dos Dados")
univariada = st.Page("uni.py", title = "Etapa 3: Descritiva Básica Univariada")
bivariada = st.Page("biv.py", title = "Etapa 4: Descritiva Bivariada")
tratamento = st.Page("trat.py", title = "Etapa 5: Tratamento dos dados")
agrupamento = st.Page("ag.py", title = "Etapa 6: Agrupamento de Cateogorias")
equacao = st.Page("equacao.py", title = "Etapa 7: Modelagem")
avaliacao = st.Page("aval.py", title = "Etapa 8: Avaliação do Modelo")

st.navigation([intro, dados, univariada, bivariada, tratamento, agrupamento, equacao, avaliacao]).run()