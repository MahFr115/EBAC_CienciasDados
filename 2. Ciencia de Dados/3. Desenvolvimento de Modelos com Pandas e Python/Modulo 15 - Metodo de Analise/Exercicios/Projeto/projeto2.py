import streamlit as st

st.set_page_config(page_title="Projeto 2", page_icon="📊")

intro = st.Page("intro.py", title = "Etapa 1: Entedimento do Negócio")
dados = st.Page("dados.py", title = "Etapa 2: Entedimento dos Dados")
clean = st.Page("clean.py", title = "Etapa 3: Preparação dos Dados")
molde = st.Page("molde.py", title = "Etapa 4: Modelagem")
aval = st.Page("aval.py", title = "Etapa 5: Avaliação dos Resultados")

pg = st.navigation([intro, dados, clean, molde, aval])

pg.run()
