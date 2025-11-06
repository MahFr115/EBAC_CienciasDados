import streamlit as st

import pandas as pd
import numpy as np

import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy.stats import ks_2samp
from sklearn import metrics
import os

st.title("Ciências de Dados - EBAC")
st.header("Avaliação do Modelo")

file_path = os.path.join(os.path.dirname(__file__), 'credit_scoring.ftr')
df = pd.read_feather(file_path)
df["tempo_emprego"] = df["tempo_emprego"].fillna(df.groupby(["tipo_renda"])["tempo_emprego"].transform("mean"))

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



formula = '''
    mau ~ I(idade**2) + I(-tempo_emprego) + I(1/renda) 
'''

rl = smf.glm(formula, data=train, family=sm.families.Binomial()).fit()

oot = df[pd.to_datetime(df.data_ref) > pd.to_datetime(df.data_ref.max()) - pd.DateOffset(months=3)]

#############################################
st.write("Avaliando o poder discriminante do modelo pelo menos avaliando acurácia, KS e Gini. Utiizando essas métricas nas bases de desenvolvimento e out of time. Análise realizado com o código:")

st.code('''oot['score'] = rl.predict(oot)

# Acurácia
acc = metrics.accuracy_score(oot.mau, oot.score>.068)
#AUC
fpr, tpr, thresholds = metrics.roc_curve(oot.mau, oot.score)
auc = metrics.auc(fpr, tpr)
#Gini
gini = 2*auc -1
ks = ks_2samp(oot.loc[oot.mau == 1, 'score'], oot.loc[oot.mau != 1, 'score']).statistic

print('Acurácia: {0:.1%} \nAUC: {1:.1%} \nGINI: {2:.1%}\nKS: {3:.1%}'
      .format(acc, auc, gini, ks))
''', language = "python")


oot['score'] = rl.predict(oot)

# Acurácia
acc = metrics.accuracy_score(oot.mau, oot.score>.068)
#AUC
fpr, tpr, thresholds = metrics.roc_curve(oot.mau, oot.score)
auc = metrics.auc(fpr, tpr)
#Gini
gini = 2*auc -1
ks = ks_2samp(oot.loc[oot.mau == 1, 'score'], oot.loc[oot.mau != 1, 'score']).statistic

st.write("Acurácia: {0:.1%}".format(acc)) 
st.write("AUC: {0:.1%}".format(auc))
st.write("GINI: {0:.1%}".format(gini))
st.write("KS: {0:.1%}".format(ks))


st.write("Apesar da consistência estatística, as métricas de desempenho preditivo indicam baixa capacidade discriminatória. O modelo final apresentou acurácia de 14,5%, AUC de 26,7% e índice de Gini negativo (-46,6%), sugerindo que o modelo está classificando de forma inversa em relação à realidade observada. O KS (Kolmogorov–Smirnov) de 33,8% demonstra alguma separação entre bons e maus pagadores, porém ainda insuficiente para caracterizar um bom poder preditivo.")

st.write("Esses resultados indicam que, embora o modelo esteja estatisticamente ajustado e teoricamente coerente, sua performance preditiva é insatisfatória, demandando ajustes adicionais — como revisão de variáveis explicativas, novos tratamentos de outliers ou o uso de técnicas não lineares mais robustas (como árvores de decisão ou modelos de ensemble) para capturar padrões mais complexos nos dados.")