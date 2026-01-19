import streamlit as st
import pandas as pd
import numpy as np
import pickle

df_art = pd.read_csv('../data/processed/base_artista_simulador.csv')
lista_generos = sorted(df_art['generos'].unique())

locais = pd.read_csv('../data/raw/locais_limpo.csv')
locais['Capacidade'] = pd.to_numeric(locais['Capacidade'])

df = pd.read_csv('../data/processed/base_modelo.csv')
avatar = 'avatar_simulador.jpg'

model = pickle.load(open('../data/models/modelo_final.pkl', 'rb'))
reference_columns = pickle.load(open('../data/models/reference_columns.pkl', 'rb'))

def preprocess_input(df_input, reference_columns):
    categoricas = ['genero_cluster', 'tipo_dia', 'mes']
    df_dummies = pd.get_dummies(df_input[categoricas], drop_first=True)
    
    numericas = [col for col in df_input.columns if col not in categoricas]
    df_processed = pd.concat([df_input[numericas], df_dummies], axis=1)
    
    df_processed = df_processed.reindex(columns=reference_columns, fill_value=0)
    
    return df_processed

#######################################################################################################

st.title("🎶 Previsão de Demanda para Shows Musicais em São Paulo")
st.header("🏟️ Simulador de Público")

st.markdown("""

Nessa seção apresento o simulador de predição de público em shows, objetivo final do projeto desenvolvido.

**Objetivo:** Entender o comportamento de público em shows médios e grandes em SP, analisando impacto de:
- Popularidade no Spotify
- Gênero musical
- Local do evento
**Período analisado:** 2022 a 2025 (pós-pandemia até boom atual)  
**Total de shows analisados:** ~900 eventos únicos  
""")
#######################################################################################################
st.title("🎯 Simulador de Lotação de Shows")

st.markdown("Selecione as características do show e veja a **lotação prevista** pelo modelo.")
st.markdown("#### Dados do Artista")

col1, col2 = st.columns([1, 1])  

with col1:
    genero = st.selectbox("Gênero musical", 
    options=lista_generos, index = None, help = """Selecione 
    o gênero musical do artista ou banda""")
    if genero is None:
        genero_cl = None
    else:
        genero_cl = (df_art.loc[df_art['generos'] == genero, 'genero_cluster'].astype(str).iloc[0])


with col2:
    generos_info = df_art[df_art['generos'] == genero]   
    lista_artistas = sorted(generos_info['nome'].unique())
   
    artista = st.selectbox("Selecione o artista", index = None, 
    options=lista_artistas, help = """Selecione o nome do 
    artista ou banda""")

art_sel = generos_info[generos_info['nome'] == artista]

col3, col4, col5 = st.columns([1, 2, 1])
with col4:
    
    if artista != None:
        st.markdown(f"""<div style=" background-color: #F1FBFC; color: #00ACC1; padding: 18px; border-radius: 12px; text-align: center;
        font-size: 20px; font-weight: 600; line-height: 1.6; box-shadow: 0 4px 10px rgba(0, 172, 193, 0.15);">
        <b>{artista}<b>
        </div><br>""", unsafe_allow_html=True)
        popularidade_real = art_sel['popularidade'].iloc[0]
        seguidores_real = art_sel['seguidores'].iloc[0]

        url_imagem = df_art.loc[df_art['nome'] == artista, 'imagem'].iloc[0]
        if url_imagem and url_imagem.strip() != 'None':
            try:
                st.image(url_imagem)
            except:
                st.image(avatar)
        else:
            st.image(avatar)

        st.markdown(f"""<div style="background-color: #F1FBFC; color: #00ACC1; padding: 18px; border-radius: 12px; font-size: 16px; 
        font-weight: 600; line-height: 1.6; box-shadow: 0 4px 10px rgba(0, 172, 193, 0.15);">
        <b>Popularidade (Spotify)</b>: {popularidade_real}/100<br>
        <b>Seguidores</b>: {seguidores_real:,.0f}
        </div>""", unsafe_allow_html=True)
    else: 
        st.image(avatar)


st.container()
st.container()

st.markdown("#### Parâmetros do Show")
col6, col7, col8, col9, col10 = st.columns([1, 1, 1, 1, 1])
with col7:
    ano = st.slider("Ano", 2026, 2035, 2030)
with col8: 
    ordem_meses = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'MAIO', 
    'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 
    'NOVEMBRO', 'DEZEMBRO']
    mes = st.selectbox("Mês", options=ordem_meses)
with col9:
    distancia = st.slider("""Dias entre outro show do mesmo 
    gênero""", 730, 0, 730, format="%d dias")
    nao_sei = st.checkbox("""Dado não conhecido / Sem 
    histórico recente""", value=False, help="""Marque se não 
    tiver essa informação. O modelo usará um valor estimado."""
    )
    if nao_sei:
        dist = 999
    else:
        dist = distancia

st.container()

#######################################################################################################
#  Previsão
if st.button("🔮 Prever Lotação", type="primary"):

    if artista is None:
        st.error("Selecione um artista antes de prever.")
        st.stop()
    
    else:
        with st.spinner("Calculando previsão..."):
            try:
                ano_int = int(ano)
                
                popularidade_float = float(popularidade_real)
                dist_float = float(dist) if dist is not None else 0.0

                input_data = pd.DataFrame({
                    'ano': [int(ano)],
                    'popularidade': [float(popularidade_real)],
                    'genero_cluster': [str(genero_cl)],              
                    'mes': [str(mes)],                      
                    'distancia_dias_anterior': [float(dist)]                                
                })

                pred = model.predict(input_data)[0]

                pred = min(pred, 150000)

                st.markdown(f"# 🎪 Lotação Prevista")

                if pred < 15000:
                    local_tipo = "Casa de Show Média"
                    locais = locais[locais['Categoria_Local'] == 'MEDIAS CASAS']
                
                elif pred >= 15000 & pred < 40000:
                    local_tipo = "Casa de Show Grande"
                    locais = locais[locais['Categoria_Local'] == 'GRANDES CASAS']

                elif pred >=40000:
                    local_tipo = "Arena ou Estádio"
                    locais = locais[locais['Categoria_Local'] == 'ARENAS E ESTADIOS']

                if 'Capacidade' in locais.columns:
                    locais['Capacidade'] = pd.to_numeric(locais['Capacidade'] ,errors='coerce')
                    mask_valid = locais['Capacidade'] > 0
                    locais['lotacao_pct'] = 0.0
                    locais.loc[mask_valid, 'lotacao_pct'] = (pred / locais.loc[mask_valid, 'Capacidade']) * 100
                    top_locais = locais.sort_values('lotacao_pct').head(2)
                else:
                    top_locais = locais.head(2)
                    st.warning("Sem coluna 'Capacidade' → % de lotação não calculado")

                st.markdown(f"Previsão para **{artista}** em {mes}/{ano}")
                st.metric("Público estimado", f"{int(pred):,} pessoas")
                st.markdown(f"**Categoria de local sugerida:** {local_tipo}")

                if not top_locais.empty:
                    st.markdown("**Duas melhores opções de locais (ordenadas por conforto de lotação):**")
                    
                    for _, row in top_locais.iterrows():
                        nome = row.get('nome_local', 'Nome não cadastrado')
                        cap = row.get('Capacidade', None)
                        lotacao_esperada = int(pred) if pred is not None else 0
                        
                        # Calcula % de lotação para este local
                        if cap and pd.notna(cap) and cap > 0:
                            pct_local = (lotacao_esperada / cap) * 100
                        else:
                            pct_local = None
                        
                        # Mostra o nome do local e lotação prevista
                        st.markdown(f"• **{nome}** (capacidade ≈ {cap}) → Lotação prevista: **{lotacao_esperada:,} pessoas**")
                        
                        # Avaliação qualitativa individual
                        if pct_local is not None:
                            if pct_local >= 95:
                                st.success(f"🎉 Sold out ({pct_local:.2f}%) provável em {nome}!")
                            elif pct_local >= 80:
                                st.success(f"✅ Alta lotação ({pct_local:.2f}%) — ótimo retorno esperado em {nome}")
                            elif pct_local >= 60:
                                st.info(f"⚠️ Lotação razoável ({pct_local:.2f}%) — ainda há espaço em {nome}")
                            else:
                                st.warning(f"❌ Lotação baixa ({pct_local:.2f}%) — considere divulgação ou ajustes em {nome}")
                        else:
                            st.info(f"Avaliação qualitativa não disponível para {nome} (capacidade não informada)")

            except Exception as e:
                st.error("Erro na previsão ou cálculo.")
                st.code(str(e))