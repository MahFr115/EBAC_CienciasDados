import streamlit as st
import pandas as pd
import numpy as np
import chardet
import unicodedata
import time

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

import json
import base64
from dotenv import load_dotenv

import matplotlib.pyplot as plt
import seaborn as sns
from phik.report import plot_correlation_matrix

from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report  

st.title("🎶 Previsão de Demanda para Shows Musicais em São Paulo")

st.header(" 🎲 Entendimento e Construção da Base de Dados")

st.markdown("""
## Descrição inicial

Objetivando-se estimar o público presente em shows médios e grandes a base de dados construída para o desenvolvimento do projeto procura 
descrever locais, datas, artistas e históricos de shows passados. 

Para entendimento inicial é preciso, anteriormente, entender distinções iniciais desenvolvidos para o recorte:
 * Shows Médios e Grandes: Shows ocorridos em locais que comportam a presença de uma público igual ou maior que 2000 pessoas
 * Artistas relevantes para o estudo: Artistas com popularidade maior ou igual a 50 e seguidorees maior oou igual 150000 no Spotify, 
 independeten do genêro ou região de origem.
 * Headliners: Pricipais artistas da noite em festivias.
 * Período Pós-Pandemia: Datas posteriores ao dia 01/01/2021
""")

database = st.selectbox(
    "Escolha a processo que deseja explorar", 
    options=['Normalização', 'Artistas', 'Calendário', 'Festivais', 'Lista de Shows', 'Locais', 'Setores', 'Shows Inicialmente Tratada', 
    'Público Estimado por Show', 'Valores por Setor',  'Base para Analise', 'Base Final de Artistas', 'Base de Desenvolvimento para Modelagem'],
    index = None          
)

if database == "Calendário":
    cal_i = pd.read_csv('../data/external/calendario_sp.csv')
    cal_f = pd.read_csv('../data/raw/calendario_tratado.csv')

    st.markdown("""
        ### Base de Calendário e Condições Climáticas

        Essa base contém informações diárias de **2021 a 2025** em São Paulo, com foco em características temporais e meteorológicas relevantes para a análise de público em shows.

        **Total de registros:** 2.192 dias  
        **Objetivo:** Enriquecer a base de shows com variáveis de data, feriados e clima.

        #### Construção da Base de Datas
        Utilizou-se o `pandas.date_range` para gerar todas as datas do período:

        ```python
        st_date = "2021-01-01"
        end_date = "2025-12-31"
        dates = pd.date_range(start=st_date, end=end_date, freq="D")
        dt = pd.DataFrame({"data": dates})
        dt["ano"] = dt["data"].dt.year
        dt["dia_semana"] = dt["data"].dt.day_name(locale="pt_BR")
        ```
        #### Inclusão de Feriados

        * Feriados nacionais: Obtidos via BrasilAPI para cada ano.
        * Feriados municipais e estaduais: Inseridos manualmente:
            * Aniversário de São Paulo (25/01)
            * Revolução Constitucionalista (09/07)
            * Consciência Negra (20/11 — até 2023)

        #### Classificação do Tipo de Dia

        ```python
        Pythondt.loc[dt["data"].dt.weekday >= 5, "tipo_dia"] = "Fim de semana"
        dt["tipo_dia"] = dt["tipo_dia"].fillna("Dia útil")
        dt["tipo_dia"] = np.where(dt["nome_feriado"].notna(), "Feriado Nacional", dt["tipo_dia"])
        ```

        #### Dados Climáticos
        Obtidos via Open-Meteo API (gratuita e histórica):
        * Temperatura máxima e mínima
        * Precipitação total (mm)
        * Código meteorológico (WMO)

        Tradução do código para descrição textual:
        
        ```python
        Pythonweather_map = {
            0: "Céu limpo", 1: "Predominantemente limpo", 2: "Parcialmente nublado", 3: "Nublado",
            51: "Chuvisco leve", 53: "Chuvisco moderado", 55: "Chuvisco intenso",
            61: "Chuva leve", 63: "Chuva moderada", 65: "Chuva forte",
            # ... demais códigos
        }
        dt["descricao_clima"] = dt["weathercode"].map(weather_map)
        ```

        #### Tratamento de Valores Ausentes

        * 415 registros sem dados climáticos (provavelmente falhas na API).
        * Preenchimento com média mensal das variáveis climáticas.
        * Criação da coluna temperatura_media.

        Variáveis Finais

        | Variável              | Descrição                                      |
        |-----------------------|------------------------------------------------|
        | data                  | Data completa                                  |
        | ano                   | Ano                                            |
        | mes                   | Nome do mês (Janeiro a Dezembro)               |
        | dia_semana            | Nome do dia da semana                          |
        | tipo_dia              | "Dia útil", "Fim de semana" ou "Feriado Nacional" |
        | nome_feriado          | Nome do feriado (se aplicável)                 |
        | precipitacao_sum      | Volume de chuva (mm)                           |
        | temperatura_media     | Temperatura média do dia (°C)                   |
        | descricao_clima       | Condição climática em texto legível            |

        Visualização da base de dados inicial
    """)
    st.dataframe(cal_i.head())

    cal_in = cal_i.to_csv(index=False).encode('utf-8')
    st.download_button(
    label="⬇️ Download da Base Inicial",
    data=cal_in,
    file_name="calendario_sp.csv",
    mime="text/csv"
    )

    st.markdown("""
        ### Limpeza Inicial
            O profile report interativo da base de dados encontrado está apresentado abaixo:
    """)

    if st.button("Gerar Profile Report"):
        profile = ProfileReport(cal_i, title="Profile Report - Calendário Inicial", explorative=True)
        st_profile_report(profile)

    st.markdown("""
        Matriz de correlação entre as variáveis dessa base
    """)

    fig, ax = plt.subplots(figsize=(10, 8))
    corr = cal_i.select_dtypes(include=['float64', 'int64']).corr()
    sns.heatmap(corr, annot=True, cmap='vlag', center=0, linewidths=1, ax=ax, fmt=".2f")
    plt.title("Correlação entre Variáveis Numéricas (Calendário)", color='#6A1B9A', fontsize=16, pad=20)
    st.pyplot(fig)

    st.markdown("""Decisões de exclusão:

        * weathercode foi mantido apenas para referência interna (descricao_clima é mais interpretável).
        * num_mes foi removido por redundância com a coluna mes.
    
    Por fim a base foi dimensionalizada para manter o valor de data unitário. O resultado final pode ser observado a seguir:
    """)

    st.dataframe(cal_f.head())
    cal_fi = cal_f.to_csv(index=False).encode('utf-8')
    st.download_button(
    label="⬇️ Download da Base Tratada",
    data=cal_fi,
    file_name="calendario_tratado.csv",
    mime="text/csv"
    )
    st.markdown("""
    Essa base foi posteriormente mesclada com a base de shows por data, permitindo análise do impacto do clima e do tipo de dia na lotação.
    """)
    

elif database == "Lista de Shows":
    shows_i = pd.read_csv('../data/external/shows.csv')
    shows_f = pd.read_csv('../data/raw/shows_limpo.csv')
    st.markdown("""
    ### Lista de Shows

   Essa base contém a **listagem completa de shows** coletados em São Paulo entre 2021 e 2025, antes da filtragem por porte do evento.
    
    **Total de registros:** 10620 shows.  
    
    **Objetivo:** Servir como ponto de partida para seleção dos shows médios e grandes que compõem o escopo final do projeto.

    ### Fontes e Construção
    - **Coleta inicial**: API do **setlist.fm** (setlists de shows ao vivo).
    - Busca por cidade = "São Paulo", estado = "SP", anos 2021–2025.
    - Tratamento de rate limit e erros da API com pausas e retries.
    """)

    st.code("""
        # Definições
        pais = "BR"
        city = "São Paulo"
        uf = "SP"
        shows = []

        for ano in range(2021, 2026):
            pagina = 1
            total_paginas = 0  # Para rastrear

            while pagina <= 150:  # Limite razoável por ano (SP tem ~200–600 shows/ano)
                try:
                    url = "https://api.setlist.fm/rest/1.0/search/setlists"
                    headers = {
                        "x-api-key": api_key,
                        "Accept": "application/json"
                    }
                    params = {
                        "cityName": city,
                        "countryCode": pais,
                        "stateCode": uf,
                        "p": pagina,
                        "year": ano
                    }

                    resp = requests.get(url, headers=headers, params=params, timeout=30)

                    # Rate limit
                    if resp.status_code == 429:
                        print(f"⚠️ Rate limit no ano {ano}, página {pagina}. Aguardando 60s...")
                        time.sleep(60)
                        continue

                    # 404 ou vazio = sem mais resultados para esse ano
                    if resp.status_code == 404:
                        print(f"✅ Ano {ano} concluído na página {pagina} (404 = sem mais dados)")
                        break
                    elif resp.status_code == 200:
                        data = resp.json()
                        setlists = data.get("setlist", [])

                        if not setlists:  # Lista vazia também para o loop
                            print(f"✅ Ano {ano} concluído na página {pagina} (lista vazia)")
                            break

                        print(f"Ano {ano} | Página {pagina}: +{len(setlists)} shows coletados")

                        # Processa shows
                        for s in setlists:
                            try:
                                data_show = pd.to_datetime(s["eventDate"], format="%d-%m-%Y", errors="coerce")
                                if pd.notna(data_show) and data_show.year == ano:
                                    shows.append({
                                        "artista": s["artist"]["name"],
                                        "data": data_show.date(),
                                        "ano": data_show.year,
                                        "local": s["venue"]["name"],
                                        "cidade": s["venue"]["city"]["name"],
                                        "estado": s["venue"]["city"].get("state", "SP")  # Adicionei para completude
                                    })
                            except:
                                continue

                        pagina += 1
                        time.sleep(1.5)
                except:
                    break

        df_shows = pd.DataFrame(shows)
    """, language = 'python'
    )

    st.write("""### Variáveis da Base Inicial

| Variável              | Descrição                                                |
|-----------------------|----------------------------------------------------------|
| artista               | Nome do Artista ou banda                                 |
| data                  | Data do show                                             |
| ano                   | Ano  do show                                             |
| local                 | Nome do local do evento                                  |
| cidade                | Cidade do evento (coluna de controle)                    |
| estado                | Estado do evento (coluna de controle)                    |

    """)
    st.write("""Visualização da base de dados inicial""")
    st.dataframe(shows_i.head())

    shows_in = shows_i.to_csv(index=False).encode('utf-8')
    st.download_button(
    label="⬇️ Download da Base Inicial",
    data=shows_in,
    file_name="shows_inical.csv",
    mime="text/csv"
    )

    st.write("""
        ### Limpeza Inicial
        Na base de dados inicial houve valores nulos na coluna de local, esses "não valores" foram substituidos pela moda de local em 
        relação ao artista do show, utilizando o código:""")

    st.code('''fill_mode = lambda x: x.fillna(x.mode()[0])
 shows['local'] = shows.groupby('artista')['local'].transform(
    lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else 'Desconhecido')
 ''', language = 'python')

    st.write("""As nomenclaturas foram padronizadas utilizando o código apresentado na seção referente.

 O profile report interativo da base de dados encontrado está apresentado abaixo:
    """)

    if st.button("Gerar Profile Report"):
        profile = ProfileReport(shows_i, title="Profile Report - Base Inicial de Shows", explorative=True)
        st_profile_report(profile)

    st.markdown("""### Decisões de exclusão:

    * O profile indica a existencia de dados duplicados, como serão considerados apenas shows grandes e médios para a análise do trabalho, foi considerado impossível o mesmo artista fazer um show em um mesmo local em um mesmo dia. Assim, foram apagadas as linhas duplicadas dessa base. 
    * Shows em municípios diferentes de São Paulo foram apagados.
    * Como as colunas de estado e cidade estavam presente apenas para controle ambas forma apagadas.
    * Considerando a normalização dos nomes, as colunas de nomenclaturas não normalizadas foram, também, apagadas.

    Assim a base de dados resultante desse tratamento é apresentada a seguir:
    """)

    st.dataframe(shows_f.head())

    shows_fi = shows_f.to_csv(index=False).encode('utf-8')
    st.download_button(
    label="⬇️ Download da Base Tratada",
    data=shows_fi,
    file_name="shows_tratado.csv",
    mime="text/csv"
    )


elif database == "Artistas":
    artistas_i = pd.read_csv('../data/external/artistas.csv', sep=';', encoding='latin1')
    st.markdown("""
    ### Lista de Artistas
    
    Essa base contém uma **listagem inicial de artistas** de interesse para o desenvolvimento das predições do estudo.
    **Total de registros (base inicial):** 4.757 artistas 
    **Objetivo:** Servir como ponto de partida para determinação da popularidade do artista ou banda perante o público.
    
    #### Fontes e Construção 
    
    - **Coleta inicial**: **Spotify Web API** (principal plataforma mundial de streaming de áudio). 
    - Busca realizada em múltiplas rodadas com critérios: 
        - Popularidade > 50 
        - Seguidores > 150.000 
    - Gêneros brasileiros relevantes (sertanejo, funk, pagode, trap, etc.) 
    - Busca por letras e números para capturar artistas locais menos populares
    
     código foi executado em várias etapas para contornar limites da API:
    """)
    
    st.code("""
        GENRES = [
        "sertanejo pop", "sertanejo", "sertanejo universitario", "arrocha", "country", "forro", "funk carioca", "funk mtg", "brega funk", "pagode", "pagode baiano", "samba", "mpb", "brazilian", "bossa nova", "brazilian hip hop", "trap brasileiro", "trap", "drill brasileiro", "pop", "brazilian pop", "pop nacional", "rock", "brazilian rock", "indie", "indie rock", "emo", "pop punk", "punk rock", "metal", "brazilian metal", "eletronica", "brazilian edm", "bass house", "deep house", "reggaeton", "latin pop", "latin", "urbano latino", "rap", "hip hop", "trap latino", "drill", "k-pop", "afrobeats", "r&b", "dance pop"
        ]
        # Divisão em blocos para usar múltiplas credenciais 
        API GENRES_1 = GENRES[:len(GENRES)//2] 
        GENRES_2 = GENRES[len(GENRES)//2:]
        LETTERS_1 = list(string.ascii_uppercase)[:13] 
        LETTERS_2 = list(string.ascii_uppercase)[13:] 
        NUM = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        LIMIT = 50 
        MAX_PAGES = 10 
        MIN_POPULARITY = 59 
        MIN_FOLLOWERS = 150000

        # Funções de autenticação, coleta e salvamento incremental (evitando perda por timeout)

        def extract_from_item(a, fonte):
            followers = a.get("followers", {}).get("total", 0)
            genres = ", ".join(a.get("genres", []))
            images = a.get("images", [])
            image_url = images[0]["url"] if images else ""
            return {
                "nome": a.get("name", ""),
                "id_spotify": a.get("id", ""),
                "generos": genres,
                "popularidade": a.get("popularity", 0),
                "seguidores": followers,
                "imagem": image_url,
                "fonte": fonte
            }

        def coletar(sp, query_list, fonte_label):
            todos = load_parcial()

            for termo in query_list:
                print(f"\n🎧 Termo: {termo}")
                for pag in range(MAX_PAGES):
                    try:
                        r = sp.search(
                            q=termo,
                            type='artist',
                            limit=LIMIT,
                            offset=pag * LIMIT
                        )
                        items = r.get("artists", {}).get("items", [])

                        if not items:
                            break

                        for a in items:
                            if a.get("popularity", 0) < MIN_POPULARITY:
                                continue
                            seg = a.get("followers", {}).get("total", 0)
                            if seg >= MIN_FOLLOWERS:
                                todos.append(extract_from_item(a, fonte_label))

                            if len(todos) % 50 == 0:
                                save_parcial(todos)

                        time.sleep(random.uniform(1.3, 2.4))

                    except Exception as e:
                        print("⚠️ Erro:", e, "→ aguardando 8s...")
                        time.sleep(8)
            save_parcial(todos)
            print("✔ Coleta concluída para esse bloco.")
            return todos

        if __name__ == "__main__":
            # BLOCO 1 – GENRES_1
            sp = autenticar(0)
            coletar(sp, [f'genre:"{g}"' for g in GENRES_1], "GENRE_1")
        …
    """, language = 'python')
    st.markdown("""
    Esse código foi rodado, aproximadamente, 6 vezes para se chegar na base de dados inicial apresentada.
        
    ### Variáveis da Base Inicial

| Variável              | Descrição                                                |
|-----------------------|----------------------------------------------------------|
| nome                  | Nome do artista ou banda                                 |
| id_spotify            | ID único do artista no Spotify                           |
| generos               | Gêneros musicais associados (separados por vírgula)      |
| Popularidade          | Índice de popularidade no Spotify (0–100)                |
| seguidores            | Número total de seguidores no Spotify                    |
| imagem                | URL da imagem de perfil do artista                       |
| fonte                 | Etapa da coleta em que o artista foi encontrado          |
        """)

    st.markdown(""" Visualização da base de dados inicial""")
    st.dataframe(artistas_i.head())

    artistas_in = artistas_i.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base Inicial",
        data= artistas_in,
        file_name="artistas_inical.csv",
        mime="text/csv"
    )

    st.markdown("""
        ### Limpeza e Tratamento Inicial

        **Padronização de nomes**: Normalização para merge correto com a base de shows. \n
        **Remoção de duplicatas**: Baseado no id_spotify. \n
        **Filtragem**: Mantidos apenas artistas com dados completos relevantes.\n

        O profile report interativo da base de dados encontrado está apresentado abaixo:
        """)
        
    if st.button("Gerar Profile Report"):
        profile = ProfileReport(artistas_i, title="Profile Report - Artistas Inicial", explorative=True)
        st_profile_report(profile)


elif database == "Locais":
    locais_i = pd.read_csv('../data/external/locais.csv', sep=';', encoding='latin1')
    locais_f = pd.read_csv('../data/raw/locais_limpo.csv')

    st.markdown("""
        ### Lista de Locais

        Essa base contém informações dos **principais locais** onde eventos musicais são realizados em São Paulo.

        **Total de registros:** 71 locais  
        **Objetivo:** Enriquecer e filtrar a base de shows com variáveis em relação aos locais de eventos .

        #### Fontes e Construção 
        - **Coleta inicial**: Considerados os dados referentes ao item "venue id" do site setlistfm. 
        - Critérios de inclusão (pesquisa manual): 
            - Capacidade minima de público: 2000 pessoas 
            - Município: São Paulo

        ### Variáveis da Base Inicial

        | Variável              | Descrição                                   |
        |-----------------------|---------------------------------------------|
        | Local_ID              | ID único do espaço de evento                |
        | Nome_Local            | Nome oficial do local                       |
        | Capacidade            | Capacidade média de público                 |
        | Categoria_Local       | Classificação por porte (Arenas/Estádios, Grandes Casas, Médias Casas) |
        | Tipo_Espaco           | Classificação por uso (estádio, casa de shows, arena multiuso, etc.) |
        | Bairro                | Bairro ou região do local                   |
        | Latitude              | Coordenada geográfica                       |
        | Longitude             | Coordenada geográfica                       |

        Visualização da base de dados inicial
    """)
    
    st.dataframe(locais_i.head())

    locais_in = locais_i.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base Inicial",
        data= locais_in,
        file_name="locais_inical.csv",
        mime="text/csv"
    )

    st.markdown(""" 
        - **Normalização** de nomes de locais, categorias e tipos de espaço.
        - **Validação** de coordenadas geográficas (latitude/longitude).
        
        O profile report interativo da base de dados encontrado está apresentado abaixo:
    """)

    if st.button("Gerar Profile Report"):
        profile = ProfileReport(artistas_i, title="Profile Report - Locais", explorative=True)
        st_profile_report(profile)

    st.markdown(""" 
    #### Matriz de Correlação (Variáveis Numéricas)
        A matriz de relação entre variáveis foi criadda para entendimento da relevância de se manter cada um dos dados coletados. Como a base é 
        composta em sua grande maioria por variáveis categóricas utilizarei a análise Phik para estudo
    """)

    fig, ax = plt.subplots(figsize=(10, 8))
    phik_corr = locais_i.phik_matrix(interval_cols=[])
    sns.heatmap(
        phik_corr,
        annot=True,
        fmt='.2f',
        cmap='vlag',             
        center=0,
        linewidths=2,
        linecolor='#FFFFFF'
    ) 
    plt.title('Matriz de Correlação (Phik)', color='#6A1B9A', fontsize=14, pad=20)

    st.pyplot(fig)

    st.markdown("""Decisões de exclusão:

* Local_ID foi mantido apenas para referência interna (descricao_clima é mais interpretável).
* Bairro foi removido por redundância com as colunas Latitude e Longitude.
 
O resultado final pode ser observado a seguir:
    """)

    st.dataframe(locais_f.head())
    locais_fi = locais_f.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base Tratada",
        data=locais_fi,
        file_name="locais_tratado.csv",
        mime="text/csv"
    )
    st.markdown("""
    Essa base foi posteriormente mesclada com a base de shows por data, permitindo análise do impacto do clima e do tipo de dia na lotação.
    """)


elif database == "Setores":
    set_i = pd.read_csv('../data/external/setores.csv', sep=';', encoding='latin1')
   
    st.markdown("""
        ### Lista de Setores 

        Contém informações de possíveis setores dos eventos musicais.

        **Total de registros:** 25 setores  
        **Objetivo:** detalhar os possíveis setores dos eventos.

        #### Fontes e Construção 
        - **Coleta inicial**: Considerados os dados de sites de vendas de ingressos e informações de shows. 
        - Pesquisa Manual

        ### Variáveis da Base Inicial

        | Variável              | Descrição                        |
        |-----------------------|----------------------------------|
        | Setor_ID              | ID único do setor                |
        | Nome_Setor            | Nome do Setor                    |
        | Categoria_Setor       | Classificação referente à qualidade da experiência do setor ('Comum', 'VIP', 'Luxo', 'Intermediário', 'Ultra VIP', 'Básico') |
     

        Visualização da base de dados inicial
    """)
    
    st.dataframe(set_i.head())
    set_in = set_i.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base Inicial",
        data= set_in,
        file_name="setores.csv",
        mime="text/csv"
    )

    st.markdown(""" 
        - **Normalização** de nomes dos setores.
    """) 
 

elif database == "Festivais":
    fst_i = pd.read_csv('../data/external/festivais.csv', sep=';', encoding='latin1')
    st.markdown("""
        ### Lista de Festivais 

        Contém informações dos grandes feestivias musicais ocorridos em São Paulo no período de 2021 à 2025.

        **Total de registros:** 96 festivais  
        **Objetivo:** detalhar grandes eventos e as principais atrações.

        #### Fontes e Construção 
            - **Coleta inicial**: Considerados os dados de informações de shows e grandes eventos na cidade. 
            - Pesquisa Manual

        ### Variáveis da Base Inicial

        | Variável              | Descrição                        |
        |-----------------------|----------------------------------|
        | festival              | Nome do evento                   |
        | local                 | Nome do local onde aconteceu     |
        | data                  | Data em que foi realizado        |
        | ano                   | Ano em que foi realizado         |
        | headliners            | Principais atrações da noite     |
     

        Visualização da base de dados inicial
    """)
    
    st.dataframe(fst_i.head())
    fst_in = fst_i.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base Inicial",
        data= fst_in,
        file_name="festivais.csv",
        mime="text/csv"
    )

    st.markdown(""" 
        Processos utilizados:
        - **Normalização** de nomes de locais, eventos e headliners.
        - **Formatação** das datas  
        - **Exclusão** das colunas iniciais Local, Festival, Headliners, Data e Ano
    """) 


elif database == "Valores por Setor":
    val_i = pd.read_csv('../data/external/valores.csv', sep=';', encoding='latin1')
    val_f = pd.read_csv('../data/raw/valores.csv', sep=',', encoding='latin1')
    
    st.markdown("""
        ### Lista de Valores por Setor 

        Informações dos preços por setor dos shows da base dos **Shows Inicialmente Tratada** .
 
        **Objetivo:** Listar os valores de ingressos por setor.

        #### Fontes e Construção 
        - **Coleta inicial**: Considerados os dados de sites de vendas de ingressos e informações de shows. 
        - Pesquisa Manual

        ### Variáveis da Base Inicial

        | Variável              | Descrição                        |
        |-----------------------|----------------------------------|
        | nome                  | Nome do artista ou banda         |
        | ano_x                 | Ano do evento                    |
        | nome_local            | Local do evento                  |
        | Pista                 | Valor do ingresso do setor pista |
        | Pista Premium         | Valor do ingresso do setor pista premium |
        |...                    |...                               |  

        Há uma coluna de valor de ingresso por setor. 
        A base inicial foi carregada e o download está disponível abaixo.
        
        Visualização da base de dados inicial
    """)
    
    st.dataframe(val_i.head())
    val_in = val_i.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base Inicial",
        data= val_in,
        file_name="valores.csv",
        mime="text/csv"
    )

    st.markdown("""
        ### Tratamentos Inciais
        - **Rotacionar** a base de dados nas colunas referentes aos eventos;
        - **Normalização** das nomencalturas e preço;
        - **Substituição** dos valores nulos de preço pela média dos valores em relação ao local e setor;
        - **Exclusão** dos dados que se mantiveram nulos apos a substituição anterior;
        - **Exclusão** dos dados de shows gratuitos, esses dados geram ruido no estudo devido ao comportamento incomum do público. 

        Segue-se o download da base tratada:
    """)

    st.dataframe(val_f.head())
    val_fn = val_f.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base Tratada",
        data= val_fn,
        file_name="valores.csv",
        mime="text/csv"
    )


elif database == "Público Estimado por Show":
    lot_i = pd.read_csv('../data/external/shows_lotacao.csv', sep = ";")

    st.markdown("""
        ### Público Estimado dos Shows 

        Informações do público estimado presente nos **Shows Inicialmente Tratada**.
  
        **Objetivo:** apresentar o público presente emm cada show.

        #### Fontes e Construção 
        - **Coleta inicial**: Considerados os dados de informações de shows e grandes eventos na cidade. 
        - Pesquisa Manual

        ### Variáveis da Base Inicial

        | Variável              | Descrição                        |
        |-----------------------|----------------------------------|
        | nome                  | Nome dos artistas e bandas       |
        | data                  | Data em que foi realizado        |
        | ano_x                 | Ano em que foi realizado         |
        | nome_local            | Nome do local onde aconteceu     |
        | lotacao               | Público estimado por eventos     |
     

        Visualização da base de dados inicial
    """)
    st.dataframe(lot_i.head())
    lot_in = lot_i.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base Inicial",
        data= lot_in,
        file_name="lotacao.csv",
        mime="text/csv"
    )

    st.markdown("""
        ### Tratamentos Inciais
        - **Normalização** das nomencalturas e data.
    """)


elif database == "Shows Inicialmente Tratada":
    showstt = pd.read_csv('../data/raw/shows_tratado.csv')
    nw_art = pd.read_csv('../data/external/artistas_trat.csv') 
    st.markdown("""
    A base de dados de shows passou por um processo inicial de tratamento e enriquecimento a partir da integração com bases externas de locais, artistas e festivais. 
    O objetivo principal dessa etapa foi reduzir ruídos, eliminar outliers e manter apenas eventos musicais compatíveis com o escopo da análise.

    O tratamento ocorreu nas seguintes etapas:

    **Integração com a base de locais**
    - Realizou-se a mesclagem (*merge*) entre a base de shows e a base de locais.
    - Foram mantidos apenas shows realizados em locais com capacidade ou público-alvo estimado maior ou igual a **2.000 pessoas**, caracterizando eventos de médio e grande porte.
    - Após esse filtro, a base foi reduzida para **3.731 registros**.

    **Integração com a base de artistas**
    - A base resultante foi integrada à base de artistas para inclusão de métricas de popularidade e engajamento (Spotify).
    - Essa etapa teve como objetivo a identificação e remoção de **outliers**, como:
    - artistas com baixa popularidade em locais de grande porte;
    - shows que provavelmente representam apresentações secundárias, aberturas ou participações em festivais.
    - Para casos com múltiplos artistas no mesmo dia e local, manteve-se o artista com maior nível de popularidade.

    **Integração com a base de festivais**
    - A base foi novamente integrada à base de festivais para reduzir interferências de eventos musicais secundários associados a eventos não musicais principais.
    - Essa etapa contribuiu para uma representação mais fiel de shows com público próprio e relevante para a modelagem.

    **Tratamento de valores ausentes**
    - Após as integrações, identificaram-se valores ausentes nas variáveis provenientes do Spotify.
    - Para mitigar esse problema, foi realizada uma nova consulta à API do Spotify, resultando em uma base atualizada de artistas com **83.071 registros**.
    - Os dados faltantes foram substituídos sempre que possível.
    - Shows cujos artistas permaneceram sem informações relevantes após essa etapa foram removidos da análise.

    A seguir é apresentado um exemplo da base atualizada de artistas, disponível para download.
    """)

    st.dataframe(nw_art.head())
    new_art = nw_art.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base Inicial",
        data= new_art,
        file_name="new_artistas.csv",
        mime="text/csv"
    )

    st.markdown("""
        A base atualizada de artistas foi então mesclada novamente à base de shows tratada, substituindo os valores nulos de popularidade e seguidores 
        pelas informações obtidas na nova extração via API do Spotify.

        Abaixo é apresentado um exemplo da base final de shows tratada, que serviu como insumo para as etapas de análise exploratória, modelagem preditiva 
        e construção do simulador.
        """)
    
    st.dataframe(showstt.head())
    showstt_in = showstt.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base",
        data= showstt_in,
        file_name="shows_tratados.csv",
        mime="text/csv"
    )


elif database == "Base para Analise":
    base_analise = pd.read_csv('../data/processed/base_projeto.csv')
    
    st.markdown("""
    ### Base para Análise dos Dados

    Base criada a partir da mescla das anteriores para análise inicial dos dados de estudo.

    ### Fonte e Construção 
    Para seu desenvolvimento houve a mescla entre:
    - as bases de **Shows Inicialmente Tratada** e **lotação**
    - a base de **valores**
    - a base de **setores**
    - a base de **calendário**

    ### Tratamento Inicial
    Posteriormente a essa junção alguns tratamentos foram promovidos:
    - **limpou-se** a coluna de gêneros, deixando cada artista apenas com o primeiro que aparece na listagem original,
    - **preencheu-se** a coluna de fetivais para casos de shows fora de festivais,
    - **preencheu-se** a coluna de lotação com valores de lotação média dependentes dos locais, popularidade do artista e  genero,
    - **criou-se** a coluna de lotação percentul, comparando-se o público estimado de shows com a capacidade de cada local, 
    - **criou-se** a coluna de arrecadação estimada multiplicando-se a media dos valores de ingressos pelo público estimado em cada show

    ### Decisões de Exclusão
    - **excluiu-se** todos os dados de lotação ainda em branco, após os tratamentos aplicados anteriormente
    - **excluiu-se** as colunas que duplicadas
    - **retirou-se** da base linhas duplicadas
    - **remoção dos shows de 2021** devido à capacidade reduzida dos eventos e ao impacto negativo na qualidade dos dados.

    ### Criação de Variáveis
    - **Lotação**: Percentual de público estimado em relação à capacidade do local
    ```python
    base_final['lotacao_pct'] = base_final['lotacao']/base_final['Capacidade']
    ```
    - **Arrecadação Média**: Valor médio arrecdado por shows, considerando o preço médio dos ingressos e a média do público estimado
    ```python
    base_final['arrecadacao_estimada'] = base_final['preco'] * base_final['lotacao']
    ```
    - **Dias entre shows de um mesmo gênero**:Distância, em dias, entre shows de um mesmo gênero, calculada com o objetivo de medir a saturação do público
    ```python 
    base_final['distancia_dias_anterior'] = base_final.groupby('generos')['data'].diff().dt.days
    base_final['distancia_dias_anterior'] = base_final['distancia_dias_anterior'].fillna(999)
    ```
    ### Estrutura final
    No fim a tabela manteve um total de XXX entradas, e 21 colunas com valores não nulos
    | Variável              | Descrição                        |
    |-----------------------|----------------------------------|
    | nome                  | Nome dos artistas e bandas       |
    | data                  | Data em que foi realizado        |
    | nome_local            | Nome do local onde aconteceu     |
    | Categoria_Setor       | Classificação referente à qualidade da experiência do setor ('Comum', 'VIP', 'Luxo', 'Intermediário', 'Ultra VIP', 'Básico')|
    | ano                   | Ano em que foi realizado         |
    | Categoria_Local       | Classificação por porte (Arenas/Estádios, Grandes Casas, Médias Casas)         |
    | Tipo_Espaco           | Classificação por uso (estádio, casa de shows, arena multiuso, etc.)          |
    | Latitude              | Coordenada Geográfica            |
    | Longitude             | Coordenada Geográfica            |
    | generos               | Gêneros musicais associados      |
    | popularidade          | Índice de popularidade no Spotify (0–100) |
    | seguidores            | Número total de seguidores no Spotify |
    | festival              | Nome do evento                   |
    | lotacao               | Público estimado por eventos     |
    | preco                 | Preço do ingresso por Categoria do setor|
    | dia_semana            | Nome do dia da semana            |
    | tipo_dia              | "Dia útil", "Fim de semana" ou "Feriado Nacional"|
    | descricao_clima       | Condição climática em texto      |
    | mes                   | Nome do mês (Janeiro a Dezembro)|
    | lotacao_pct           | Percentual do público estimado em relação ao tamanho da casa|
    | setor                 | Número de setores disponíveis para venda|
    | arrecadacao_estimada  | Arrecadação média estimada no evento|
     
    """)
    st.dataframe(base_analise.head())
    analise = base_analise.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base para Análise",
        data= analise,
        file_name="base_analise.csv",
        mime="text/csv"
    )


elif database == "Base Final de Artistas":
    artistas_projeto = pd.read_csv('../data/processed/artistas_projeto.csv')
    
    st.markdown("""
    ### Base Final de Artistas

    Base criada a partir da junção entre as diversas bases de artistas obtidas.

    ### Fonte e Construção 
    **Combinação** entre as bases de dados de artistas que obtive ao longo da criação e tratamento dos dados.

    ### Tratamento Inicial
    - Da mesma forma que havia feito anteriormente mantive **apenas um genêro musical** por artista.
    - **Normalização** das nomenclatura

    ### Decisões de Exclusão
    - **Remoção** das linhas com artistas duplicados
    - **Exclusão** das linhas em que não há generos para os artistas
    - **Exclusão** das colunas de controle (fonte, id_spotify e index)
    
    ### Estrutura final
    | Variável              | Descrição                                                |
    |-----------------------|----------------------------------------------------------|
    | nome                  | Nome do artista ou banda                                 |
    | generos               | Gêneros musicais associados                              |
    | Popularidade          | Índice de popularidade no Spotify (0–100)                |
    | seguidores            | Número total de seguidores no Spotify                    |
    | imagem                | URL da imagem de perfil do artista                       |

        Visualização da base de dados
    """)
    
    st.dataframe(artistas_projeto.head())
    fin_art = artistas_projeto.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base Final",
        data= fin_art,
        file_name="artistas_projeto.csv",
        mime="text/csv"
    )
    

elif database == "Base de Desenvolvimento para Modelagem":
    projeto = pd.read_csv('../data/processed/base_modelo.csv')

    st.markdown("""
    Após a análise inicial das variáveis originalmente apresentadas, em posso dos gráficos de relação entre variáveis tomou-se decisões 
    referentes ao tratamento da base original de análise

    ### Matrizes de Relação entre Variáveis
    
    """)

    st.markdown("""
    ### Decisões de Exclusão
    Assim excluiu-se as colunas com dados referentes à:
    - nome,
    - data,
    - nome_local,
    - Categoria_Setor,
    - Setor,
    - preço por setor,
    - dados de clima,
    - Tipo_Espaco, 
    - seguidores,
    - preco_medio,
    - dia_semana
    
    mantendo-se, por fim, 9 colunas na base de dados de estudo.
    """)

    st.dataframe(projeto.head())
    modelo = projeto.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download da Base Final para o Estudo",
        data= modelo,
        file_name="base_modelo.csv",
        mime="text/csv"
    )


elif database == "Normalização":
    st.markdown(""" Para normalização das nomenclaturas de local, artista, feriados entre outras presentes no desenvolvimento do projeto 
    o serguinte código foi utlizado:
    """)
    st.code(
        """ 
        def normalize(nomes):
            if pd.isna(nomes):
                return None
            nomes = str(nomes)
            
            nomes = nomes.replace("’", "'")
            nomes = nomes.replace("‘", "'") 
            nomes = nomes.replace("“", '"') 
            nomes = nomes.replace("”", '"')  
            nomes = nomes.replace("–", "-")  
            nomes = nomes.replace("—", "-") 
            nomes = nomes.replace("‐", "-") 
            
            
            nomes = unicodedata.normalize('NFKD', nomes)
            nomes = ''.join(c for c in nomes if not unicodedata.combining(c))

            nomes = re.sub(r'\s+', ' ', nomes).strip().upper()
            
            return nomes
        """, language = 'python')


else:
    st.info("""
        ### Bem-vindo à seção de Dados!

        Aqui você pode explorar em detalhes cada uma das bases de dados utilizadas no projeto.

        **Selecione uma opção no menu acima** para visualizar:
        - Descrição da base
        - Fontes utilizadas
        - Processo de coleta e tratamento
        - Estrutura das variáveis
        - Decisões tomadas durante a limpeza

        Isso ajuda a entender como os dados foram construídos antes da análise exploratória e modelagem.
        """)


