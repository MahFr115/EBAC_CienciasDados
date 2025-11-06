import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import os

st.title("Ciências de Dados - EBAC")
st.header("Análise Descritiva")

############################################################################################################
st.write("Este dataset, originado de uma instituição financeira brasileira (anonimizado para privacidade), contém dados de originação e performance de créditos entre 2015 e 2018. Ele é perfeito para modelagem de risco de inadimplência (PD - Probability of Default), com foco em 10 safras (vintages) iniciais, mas adaptado aqui para 15 safras mensais e 12 meses de performance por contrato, permitindo análises robustas ao longo do tempo.")
st.write("O dataset tem aproximadamente 750.000 registros e mais de 15 colunas, divididas em categorias principais:")

# Dados da tabela de colunas e descrições
data = {
    'Coluna': [
        'data_ref', 'index', 'sexo', 'posse_de_veiculo', 'posse_de_imovel', 
        'qtd_filhos', 'tipo_renda', 'educacao', 'estado_civil', 'tipo_residencia', 
        'idade', 'tempo_emprego', 'qt_pessoas_residencia', 'renda', 'mau'
    ],
    'Descrição': [
        'Data de referência da safra de originação do contrato.',
        'Identificador único do registro (índice interno).',
        'Gênero do cliente.',
        'Indicador de posse de veículo (0 = não, 1 = sim).',
        'Indicador de posse de imóvel (0 = não, 1 = sim).',
        'Quantidade de filhos dependentes.',
        'Tipo de renda principal do cliente.',
        'Nível de educação formal.',
        'Estado civil do cliente.',
        'Tipo de residência atual.',
        'Idade do cliente em anos na data de originação.',
        'Tempo de emprego atual em anos (pode incluir frações).',
        'Quantidade total de pessoas na residência (incluindo o cliente).',
        'Renda mensal bruta do cliente em reais (R$).',
        'Variável alvo: Indicador de inadimplência (1 = mau pagador, 0 = bom).'
    ]
}
df_table = pd.DataFrame(data)

# Exibe a tabela
st.subheader("Tabela de Colunas e Descrições")
st.table(df_table)

st.write("Essas variáveis permitem explorar padrões sazonais, construir scores de crédito e validar modelos com métricas como AUC-ROC.")
############################################################################################################

file_path = os.path.join(os.path.dirname(__file__), 'credit_scoring.ftr')
df = pd.read_feather(file_path)
st.subheader("A base de dados:")
st.write(df.head(3))

st.write("Data máxima: ", df["data_ref"].max())

st.write(df["idade"].nunique(), "valores únicos, valor mínimo de idade: ", df["idade"].min(), ", valor máximo de idade: ", df["idade"].max())
st.write(df["renda"].nunique(), "valores únicos, valor mínimo de renda: ", df["renda"].min(), ", valor máximo de renda: ", df["renda"].max())

st.write("Criarei uma coluna de referência mês/ano para identificação de dados mensais")
df["mes_ref"] = df["data_ref"].dt.strftime("%b/%y")

############################################################################################################ 
st.subheader("Amostragem")
st.write("Separaremos os três últimos meses como safras de validação out of time (oot). Utilizando o código:")
st.code('''oot = df[pd.to_datetime(df.data_ref) > pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
train = df[pd.to_datetime(df.data_ref) <= pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
''', language = "python")

oot = df[pd.to_datetime(df.data_ref) > pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
train = df[pd.to_datetime(df.data_ref) <= pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]

st.write("Para análise desconsideraremos as colunas data_ref e a index, uma vez que são colunas de identificação e referência, que não carregam nenhum significado explicativo para a base.")
train = train.drop(["index", "data_ref"], axis = 1)
oot = oot.drop(["index", "data_ref"], axis = 1)

st.write("Datas presentes na base de desenvolvimento do modelo: ", train["mes_ref"].unique())
st.write("Datas presentes na base de validação (out of time) do modelo: ", oot["mes_ref"].unique())