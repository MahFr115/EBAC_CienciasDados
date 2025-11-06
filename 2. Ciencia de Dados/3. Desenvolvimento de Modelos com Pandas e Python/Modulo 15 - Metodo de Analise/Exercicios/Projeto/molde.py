import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.feature_selection import mutual_info_regression
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

from ydata_profiling import ProfileReport
from tqdm import tqdm
from IPython.display import display, HTML

import streamlit as st
from streamlit_pandas_profiling import st_profile_report
import os

st.title("Projeto 2 - Previsão de Rendas")
st.header("EBAC: Profissão Ciências de Dados")

renda = pd.read_csv('./input/previsao_de_renda.csv')

renda = renda.drop(renda.columns[:3], axis = 1) 
renda['tempo_emprego'] = renda['tempo_emprego'].fillna(
    renda.groupby(['idade', 'tipo_renda'])['tempo_emprego'].transform('mean')
)

renda['tempo_emprego'] = renda['tempo_emprego'].fillna(
    renda.groupby(['tipo_renda'])['tempo_emprego'].transform('mean')
)

renda['tempo_emprego_por_idade'] = round(renda['tempo_emprego'] / renda['idade'], 2)

renda['renda_per_capta'] = round(renda['renda']/ renda['qt_pessoas_residencia'], 2)

renda['renda_por_tempo_emprego'] = round(renda['renda']/renda['tempo_emprego'], 2)


st.subheader("Modelagem")

st.markdown("""Considerando os modelos estudados anteriormente, durante os módulos anteriores, com essa mesma base, temosos seguintes resultados para R²:

* Modelo de Patsy para o log(renda) ~ 0,157
* Modelo Ridge com alpha = 0 ~ 0,2682
* Modelo Lasso com alpha = 0 ~ 0,2682
* Modelo Stepwise ~ 0,2680
* Modelo de Lasso com ajuste de Árvore de Regressão ~ 0,3665

percebemos que o melhor modelo observado é o com ajuste de árvore de regressão. Então, usarei esse memso modelo nessa etapa.""")

cat = ['sexo','tipo_renda','educacao','estado_civil','tipo_residencia']
num = ['idade', 'tempo_emprego', 'qtd_filhos', 'tempo_emprego_por_idade', 'renda_per_capta', 'renda_por_tempo_emprego']

X = renda[cat + num]

y = renda['renda']

for col in X.select_dtypes(include=['bool']).columns:
	X[col] = X[col].replace({False: 0, True: 1}).astype(int)

X = pd.get_dummies(X, columns=cat, drop_first=True)
X = X.astype(float).dropna()

for col in num:
	X[col] = pd.to_numeric(X[col], errors='coerce')
	X[num] = X[num].fillna(X[num].mean())

y = pd.to_numeric(y, errors='coerce').fillna(y.mean())

st.code("""scaler = StandardScaler()
X[num] = scaler.fit_transform(X[num])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)""")

scaler = StandardScaler()
X[num] = scaler.fit_transform(X[num])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

st.markdown(f"Tamanho do conjunto de treinamento: {X_train.shape[0]} linhas")
st.markdown(f"Tamanho do conjunto de teste: {X_test.shape[0]} linhas")

st.write("Alpha para modelagem em Lasso igual a 0")

alpha = 0

print("\nResultados Lasso na base de testes:") 
st.code("""model = LinearRegression() 
model.fit(X_train, y_train) 
y_pred = model.predict(X_test) 
r2 = r2_score(y_test, y_pred) 
print(f'Alpha: {alpha}, R²: {r2:.4f}')""")

model = LinearRegression() 
model.fit(X_train, y_train) 
y_pred = model.predict(X_test) 
r2 = r2_score(y_test, y_pred) 
print(f'Alpha: {alpha}, R²: {r2:.4f}')

st.write("Ajustando a árvore de regressão com diferentes hiperparâmetros")
st.text("Resultados da Árvore de Regressão na base de testes:")
st.code("""best_r2_tree = -float('inf')
best_params = None""")
best_r2_tree = -float('inf')
best_params = None
st.write("Testando combinações de profundidade máxima e mínimo de amostras por folha")
st.code("""max_depths = [None, 5, 10, 15] 
min_samples_leafs = [1, 5, 10] 

for max_depth in max_depths:
	for min_samples_leaf in min_samples_leafs:
		model = DecisionTreeRegressor(max_depth=max_depth, 					min_samples_leaf=min_samples_leaf, random_state=42)
		model.fit(X_train, y_train)
		y_pred = model.predict(X_test)
		r2 = r2_score(y_test, y_pred)
		print(f'max_depth: {max_depth}, min_samples_leaf: {min_samples_leaf}, R²: {r2:.4f}')
		if r2 > best_r2_tree:
			best_r2_tree = r2
			best_params = (max_depth, min_samples_leaf)""")

max_depths = [None, 5, 10, 15] 
min_samples_leafs = [1, 5, 10] 

for max_depth in max_depths:
	for min_samples_leaf in min_samples_leafs:
		model = DecisionTreeRegressor(max_depth=max_depth, 					min_samples_leaf=min_samples_leaf, random_state=42)
		model.fit(X_train, y_train)
		y_pred = model.predict(X_test)
		r2 = r2_score(y_test, y_pred)
		print(f'max_depth: {max_depth}, min_samples_leaf: {min_samples_leaf}, R²: {r2:.4f}')
		if r2 > best_r2_tree:
			best_r2_tree = r2
			best_params = (max_depth, min_samples_leaf)

st.write("Resultado da melhor árvore")
st.write(f'\nMelhor Árvore de Regressão: max_depth = {best_params[0]}, min_samples_leaf = {best_params[1]}')
print(f'R² na base de testes com a melhor árvore: {best_r2_tree:.4f}')
