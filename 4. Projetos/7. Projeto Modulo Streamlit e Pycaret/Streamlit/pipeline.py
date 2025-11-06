import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix
from sklearn.utils._set_output import _SetOutputMixin
import dill
from sklearn.utils import estimator_html_repr
import streamlit.components.v1 as components

##########################################################
# Código

df = pd.read_feather('credit_scoring.ftr')
X, y = df.drop(["data_ref", "index", "mau"], axis = 1), df["mau"]
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

X_train = X_train.reset_index(drop=True)
y_train = y_train.reset_index(drop=True)

num_cols = ['qtd_filhos',	
          'idade', 
          'tempo_emprego', 
          'qt_pessoas_residencia', 
          'renda']

cat_cols = ['sexo',
        'posse_de_veiculo',
        'posse_de_imovel',
        'tipo_renda',
        'educacao',
        'estado_civil',
        'tipo_residencia']

num_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', num_pipeline, num_cols),
    ('cat', cat_pipeline, cat_cols)
])


class OutlierRemover(BaseEstimator, TransformerMixin, _SetOutputMixin):
    def __init__(self, contamination=0.1, num_cols=None):
        self.contamination = contamination
        self.model = IsolationForest(contamination=self.contamination, random_state=42)
        self.num_cols = num_cols
    
    def fit(self, X, y=None):
        if self.num_cols is not None:
            X_num = X[self.num_cols].copy()
            X_num = X_num.fillna(X_num.median())
            self.model.fit(X_num)
        return self
    
    def transform(self, X):
        if self.num_cols is not None:
            X_num = X[self.num_cols].copy()
            X_num = X_num.fillna(X_num.median())
            outliers = self.model.predict(X_num)
            mask = outliers != -1
            X = X.loc[mask]
        return X

outliers = OutlierRemover(contamination=0.1)

def selecionar_variaveis(X):
    if not hasattr(X, "columns"):
        return X
    cols = [c for c in X.columns if X[c].dtype != "object" or c == "sexo"]
    return X[cols]

variaveis = FunctionTransformer(selecionar_variaveis, validate=False)

pca = PCA(n_components=5)
pipe = Pipeline(steps=[
    ('classificador', LogisticRegression())
])

pipeline = Pipeline(steps=[
    ('Preprocessamento', preprocessor),
    ('Seleção de variaveis', variaveis),
    ('Remoção de outliers', outliers),
    ('PCA', pca),
    ('Classificação', pipe)
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_train)

# Calcular a matriz de confusão
cm = confusion_matrix(y_train, y_pred)

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='pink', 
            xticklabels=['Negativo', 'Positivo'], 
            yticklabels=['Negativo', 'Positivo'])
plt.xlabel('Previsão')
plt.ylabel('Real')
plt.title('Matriz de Confusão')
plt.show()
with open('Final_Model_Pipeline_Project.pkl', 'wb') as f:
    dill.dump(pipeline, f)
with open('Final_Model_Pipeline_Project.pkl', 'rb') as f:
    pipeline_bytes = f.read()
##########################################################

st.title("🧩 Estudo dos Dados por Pipeline")

st.header("Criar um pipeline utilizando o sklearn pipeline para o preprocessamento")

st.markdown('''
---

### Pré processamento - Substituição de nulos (NaNs)

A importação e divisãodos dados a serem analisados foi realizada da mesma forma como a anterior.

Para desenvolvimento do pré processamento dos dados como pipeline utilizei as seguintes bibliotecas
''')

st.code('''
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
''', language = "python")

st.write('''E do código:''')

st.code('''
num_cols = ['qtd_filhos',	
          'idade', 
          'tempo_emprego', 
          'qt_pessoas_residencia', 
          'renda']

cat_cols = ['sexo',
        'posse_de_veiculo',
        'posse_de_imovel',
        'tipo_renda',
        'educacao',
        'estado_civil',
        'tipo_residencia']

num_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

''', language = "python")

st.write('''Combinando ambos os códigos desenvolvidos:''')
st.code('''
preprocessor = ColumnTransformer(transformers=[
    ('num', num_pipeline, num_cols),
    ('cat', cat_pipeline, cat_cols)
])
''', language = "python")

st.markdown(''' 
---
## Remoção de outliers
Aqui utilizei as seguintes bibliotecas''')
st.code('''
from sklearn.ensemble import IsolationForest
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils._set_output import _SetOutputMixin
''', language = "python")
st.code('''
class OutlierRemover(BaseEstimator, TransformerMixin, _SetOutputMixin):
    def __init__(self, contamination=0.1, num_cols=None):
        self.contamination = contamination
        self.model = IsolationForest(contamination=self.contamination, random_state=42)
        self.num_cols = num_cols
    
    def fit(self, X, y=None):
        if self.num_cols is not None:
            X_num = X[self.num_cols].copy()
            X_num = X_num.fillna(X_num.median())
            self.model.fit(X_num)
        return self
    
    def transform(self, X):
        if self.num_cols is not None:
            X_num = X[self.num_cols].copy()
            X_num = X_num.fillna(X_num.median())
            outliers = self.model.predict(X_num)
            mask = outliers != -1
            X = X.loc[mask]
        return X

outliers = OutlierRemover(contamination=0.1)
''', language = "python")
st.markdown(''' 
---
## Seleção de variáveis
Para isso as bibliotecas e código foram''')
st.code('''
from sklearn.preprocessing import FunctionTransformer
''', language = "python")

st.code('''
def selecionar_variaveis(X):
    if not hasattr(X, "columns"):
        return X
    cols = [c for c in X.columns if X[c].dtype != "object" or c == "sexo"]
    return X[cols]

variaveis = FunctionTransformer(selecionar_variaveis, validate=False)
''', language = "python")
st.markdown(''' 
---
## Redução de dimensionalidade (PCA)
Para a descomposição de PCA o código desenvolvido foi ''')
st.code('''
from sklearn.decomposition import PCA
pca = PCA(n_components=5)
''', language = "python")
st.markdown(''' 
---
## Criação de dummies
Aplicar o get_dummies() ou onehotencoder() para transformar colunas catégoricas do dataframe em colunas de 0 e 1.

* sexo
* posse_de_veiculo
* posse_de_imovel
* tipo_renda
* educacao
* estado_civil
* tipo_residencia

Por último utilizei:''')
st.code('''
from sklearn.linear_model import LogisticRegression
''', language = "python")
st.code('''
pipe = Pipeline(steps=[
    ('classificador', LogisticRegression())
])
''', language = "python")
st.markdown(''' 
---
## Pipeline
Para essa parte utilizei as seguintes bibliotecas''')
st.code('''
from sklearn.pipeline import Pipeline
''', language = "python")
st.markdown('''E o código desenvolvido para o pipeline é:''') 
st.code('''
pipeline = Pipeline(steps=[
    ('Preprocessamento', preprocessor),
    ('Seleção de variaveis', variaveis),
    ('Remoção de outliers', outliers),
    ('PCA', pca),
    ('Classificação', pipe)
])
''', language = "python")
st.write('''Então assim fica o Pipeline desenvolvido''')
st.write(pipeline.named_steps)
st.markdown(''' 
---
## Treinamento do modelo de regressão logistica
Assim utilizando o fit, o resultado final, obtido com rodando o pipeline completo é:''')

html = estimator_html_repr(pipeline)
components.html(html, height=600, scrolling=True)
st.pyplot(plt)

st.markdown(''' ## Download do Modelo de Pipeline Treinado''')

st.download_button(
    label="📥 Download",
    data = pipeline_bytes, 
    file_name = "Final Model Pipeline Project.plk",
    mime="application/octet-stream")
st.markdown('''---
## Comparação
Para comparação e análise da importancia de cada parte do pipeline desenvolvido, nessa seção o usuário de escolher quais quer ou não implementar:''')

incluir_out = st.checkbox("Remover outliers", value=True)
incluir_var = st.checkbox("Seleção de Variaveis", value=True)
incluir_pca = st.checkbox("PCA", value=True)
incluir_class = st.checkbox("Classificar Dados", value=True)

steps = [('Preprocessamento', preprocessor)]

# Pipeline Dinamico
if incluir_var:
    steps.append(('variaveis', variaveis))
if incluir_out:
    steps.append(('outlier', outliers))
if incluir_pca:
    steps.append(('pca', pca))
if incluir_class:
    steps.append(('classificacao', pipe))

pipeline_custom = Pipeline(steps)

st.write("Esse é o Pipeline customizado:",
    
pipeline_custom.named_steps)

st.write("Após treinar o Pipeline customizado os resultados obtidos foram:")
pipeline_custom.fit(X_train, y_train)

html2 = estimator_html_repr(pipeline_custom)
components.html(html2, height=600, scrolling=True)

y_pred = pipeline_custom.predict(X_train)

cmc = confusion_matrix(y_train, y_pred)

fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(cmc, annot=True, fmt='d', cmap='pink', 
            xticklabels=['Negativo', 'Positivo'], 
            yticklabels=['Negativo', 'Positivo'])
plt.xlabel('Previsão')
plt.ylabel('Real')
plt.title('Matriz de Confusão do Pipeline Personalizado')

st.pyplot(fig)

st.success("✅ Pipeline personalizado treinado!")

st.markdown(''' ## Download do Modelo de Pipeline Personalizado Treinado''')
with open('Final_Model_Personalized_Pipeline_Project.pkl', 'wb') as f:
    dill.dump(pipeline_custom, f)
with open('Final_Model_Personalized_Pipeline_Project.pkl', 'rb') as f:
    pipelinepers_bytes = f.read()

st.download_button(
    label="📥 Download",
    data = pipelinepers_bytes, 
    file_name = "Final Model Pipeline Personalizado Project.plk",
    mime="application/octet-stream")