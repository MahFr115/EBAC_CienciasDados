import streamlit as st

import pandas as pd
import numpy as np

import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn import metrics
import os

st.title("Ciências de Dados - EBAC")
st.header("Propostas de Modelagem dos Dados")

file_path = os.path.join(os.path.dirname(__file__), 'credit_scoring.ftr')
df = pd.read_feather(file_path)

train = df[pd.to_datetime(df.data_ref) <= pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]
df_ = train.drop(["index", "data_ref"], axis = 1)
des_uni = pd.DataFrame({
    "variavel": df_.columns,
    "dtype": df_.dtypes.astype(str),
    "nmissing": df_.isna().sum().values,
    "valores_unicos": df_.nunique().values
})

des_uni["tipo_var"] = des_uni["dtype"].apply(lambda x: "quantitativo" if any(t in x for t in ["float", "int"]) else "qualitativo")
des_uni["papel"] = des_uni["variavel"].apply(lambda x: "resposta" if x == "mau" else "covariavel")
des_uni["moda"] = des_uni["variavel"].apply(lambda v: df[v].mode().iloc[0] if not df[v].mode().empty else None)
des_uni["menos_comum"] = des_uni["variavel"].apply(lambda v: df[v].value_counts().idxmin() if df[v].nunique() > 0 else None)
des_uni["mínimo"] = des_uni["variavel"].apply(lambda v: round(df[v].min(), 2) if des_uni.loc[des_uni["variavel"] == v, "tipo_var"].item() == "quantitativo" else "-")
des_uni["máximo"] = des_uni["variavel"].apply(lambda v: round(df[v].max(), 2) if des_uni.loc[des_uni["variavel"] == v, "tipo_var"].item() == "quantitativo" else "-")
des_uni["média"] = des_uni["variavel"].apply(lambda v: round(df[v].mean(), 2) if des_uni.loc[des_uni["variavel"] == v, "tipo_var"].item() == "quantitativo" else "-")
des_uni = des_uni.drop(["variavel"], axis = 1)

train["tempo_emprego"] = train["tempo_emprego"].fillna(train.groupby(["tipo_renda"])["tempo_emprego"].transform("mean"))

############################################################################################################
st.write("Equação preditiva proposta")
st.write("Primeiro analisarei uma fórmula simples")
st.code('''
formula = 
    mau ~ idade + tempo_emprego  + renda + qt_pessoas_residencia


rl = smf.glm(formula, data=df_, family=sm.families.Binomial()).fit()
''', language = "python")

formula = '''
    mau ~ idade + tempo_emprego  + renda + qt_pessoas_residencia
'''

rl = smf.glm(formula, data=train, family=sm.families.Binomial()).fit()

st.write(rl.summary())
############################################################################################################
st.write("Pelos gráficos observados anteriormente percebmos que idade tem uma forma semalhante a uma equação concava de 2º grau, tempo_emprego uma equação inversa linear, qt_emprego_residencia convexa de 2º grau e em relação a renda uma hibérbole positiva")
st.code('''
formula = 
    mau ~ I(idade**2) + tempo_emprego + I(1/renda) + I(qt_pessoas_residencia**2)
''', language = "python")

formula = '''
    mau ~ I(idade**2) + tempo_emprego + I(1/renda) + I(qt_pessoas_residencia**2)
'''

rl = smf.glm(formula, data=train, family=sm.families.Binomial()).fit()

st.write(rl.summary())
############################################################################################################
st.write("Considerando os valores dos primeiros modelos excluirei da fórmula qt_pessoas_residencia por ter valor de p muito alto em ambas os resultados")
st.code('''
formula = 
    mau ~ I(idade**2) + I(-tempo_emprego) + I(1/renda) 
''', language = "python")

formula = '''
    mau ~ I(idade**2) + I(-tempo_emprego) + I(1/renda) 
'''

rl = smf.glm(formula, data=train, family=sm.families.Binomial()).fit()

st.write(rl.summary())
############################################################################################################

st.write("Foram testados trÊs modelos de regressão logística com o objetivo de avaliar o impacto das variáveis idade, tempo de emprego, renda e quantidade de pessoas na residência sobre a probabilidade de inadimplência. O primeiro modelo considerou as variáveis em sua forma original, enquanto o segundo aplicou transformações não lineares (idade², 1/renda e qt_pessoas_residencia²), visando capturar relações mais complexas entre os preditores e a variável resposta.")

st.write("Os segundo modelo apresentou melhor ajuste estatístico, com redução na deviance (de 2.4985e+05 para 2.4951e+05) e aumento do Pseudo R² de 0.04246 para 0.04301, indicando leve melhora na explicação da variância da resposta. Além disso, as variáveis transformadas (idade², tempo_emprego e 1/renda) mostraram-se altamente significativas (p < 0.001), sugerindo que essas relações não lineares descrevem melhor o comportamento dos dados.")

st.write("Por outro lado, a variável qt_pessoas_residencia, mesmo após a transformação quadrática, não apresentou significância estatística (p = 0.162) e seu impacto sobre o ajuste do modelo foi nulo. A exclusão dessa variável resultou em um modelo final mais parcimonioso, mantendo o mesmo nível de ajuste (Pseudo R² = 0.04301) e a mesma log-verossimilhança, mas com menor complexidade.")

st.write("Em síntese, o modelo final — composto por idade², tempo de emprego e renda (1/renda) — mostrou-se estatisticamente robusto, coerente com a teoria e mais eficiente, representando a melhor alternativa entre os testados. A relação entre as variáveis e a inadimplência manteve-se economicamente plausível: quanto maior a renda e o tempo de emprego, menor a probabilidade de inadimplência, enquanto a idade apresentou uma relação não linear, sugerindo que o risco é maior em faixas etárias intermediárias.")
