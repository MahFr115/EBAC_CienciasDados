import streamlit as st

st.set_page_config(page_title="Projeto", page_icon="📊")

intro = st.Page("intro.py", title = "Etapa 1: Entedimento do Projeto")
dados = st.Page("dados.py", title = "Etapa 2: Entedimento dos Dados")
fase1 = st.Page("fase1.py", title = "Etapa 3: Estudos dos dados")
pipe = st.Page("pipeline.py", title = "Etapa 4: Estudo dos Dados por Pipeline")
pct = st.Page("proj_pycaret.py", title = "Etapa 5: Estudo dos Dados por Pycaret")

st.navigation([intro, dados, fase1, pipe, pct]).run()