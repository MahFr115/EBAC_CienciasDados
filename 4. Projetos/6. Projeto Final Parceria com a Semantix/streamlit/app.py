import streamlit as st

st.set_page_config(page_title="Mercado de Shows SP 2021–2025", page_icon="🎤", layout="wide")

intro = st.Page("1intro.py", title="Introdução", icon="📌")
dados = st.Page("2dados.py", title="Fontes e Tratamento de Dados", icon="🗃️")
eda = st.Page("3eda.py", title="Análise Exploratória", icon="📊")
variaveis = st.Page("4variaveis.py", title="Relação entre Variáveis", icon="🔗")
modelagem = st.Page("5model.py", title="Modelagem e Resultados", icon="🤖")
simulador = st.Page("6simulador.py", title="Simulador de Público", icon="🎯")
conclusao = st.Page("7conclusao.py", title="Conclusão", icon="🏁")

pg = st.navigation([intro, dados, eda, variaveis, modelagem, simulador, conclusao])
pg.run()