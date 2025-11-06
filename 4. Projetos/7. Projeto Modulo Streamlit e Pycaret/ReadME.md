# 🤖 Projeto Final – Classificação Binária com PyCaret e Streamlit

Este projeto encerra a trilha de **Ciência de Dados da EBAC**, integrando os conhecimentos adquiridos em **Análise de Dados, Modelagem Preditiva e Deploy Interativo**.  
O objetivo é desenvolver um pipeline de **classificação binária** completo, utilizando **PyCaret** para automação de Machine Learning e **Streamlit** para construção de uma interface interativa.

---

## 🎯 Objetivos do Projeto

✔ Demonstrar a aplicação completa de um fluxo de Machine Learning supervisionado  
✔ Comparar modelos de classificação de forma automatizada com **PyCaret**  
✔ Interpretar e selecionar o modelo com melhor desempenho  
✔ Integrar o modelo em uma **interface interativa com Streamlit**  
✔ Permitir que o usuário explore, analise e visualize os resultados do modelo em tempo real  

---

## 📂 Estrutura do Projeto

### 🧩 Componentes principais

| Arquivo | Descrição |
|----------|------------|
| **Resultado Projeto Final.ipynb** | Notebook principal de experimentação, automação de ML e análise de performance |
| **intro.py** | Etapa 1 – Entendimento do Projeto |
| **dados.py** | Etapa 2 – Entendimento e exploração dos dados |
| **fase1.py** | Etapa 3 – Estudo e visualização dos dados |
| **pipeline.py** | Etapa 4 – Estudo do fluxo de modelagem com Pipeline manual |
| **proj_pycaret.py** | Etapa 5 – Modelagem automatizada com PyCaret |

### ⚙️ Organização da aplicação Streamlit

Cada etapa foi estruturada como uma página interativa do Streamlit, oferecendo uma experiência de navegação por fases do projeto:

```python
intro = st.Page("intro.py", title = "Etapa 1: Entendimento do Projeto")
dados = st.Page("dados.py", title = "Etapa 2: Entendimento dos Dados")
fase1 = st.Page("fase1.py", title = "Etapa 3: Estudo dos Dados")
pipe = st.Page("pipeline.py", title = "Etapa 4: Estudo dos Dados por Pipeline")
pct = st.Page("proj_pycaret.py", title = "Etapa 5: Estudo dos Dados por PyCaret")

---

## 📊 Metodologia e Pipeline
1. Entendimento do Projeto:
Revisão dos objetivos do problema e da natureza dos dados utilizados.
2. Exploração dos Dados:
Análises descritivas, limpeza e padronização das variáveis.
3. Estudo dos Dados:
Visualizações e testes iniciais de correlação entre variáveis.
4. Pipeline Manual:
Construção do fluxo tradicional de modelagem, incluindo divisão treino/teste, normalização, tuning e validação.
5. Modelagem com PyCaret:
Utilização da biblioteca PyCaret para automatizar o processo de comparação entre modelos de classificação (Logistic Regression, Random Forest, Gradient Boosting, etc.), seleção do melhor e análise das métricas.

---

## ⚙️ Tecnologias e Bibliotecas Utilizadas
| Categoria | Ferramentas |
|----------|------------|
| ** Linguagem ** | Python 3 |
| ** Automação de ML ** | PyCaret |
| ** Modelagem Tradicional ** | Scikit-Learn |
| ** Manipulação de Dados ** | Pandas, NumPy |
| ** Visualização ** | Matplotlib, Seaborn, Plotly |
| ** Interface Web ** | Streamlit |
| ** Ambiente de Desenvolvimento ** | Jupyter Notebook, VS Code |
| ** Documentação ** | Markdown |

---

## 📈 Resultados Esperados

Identificação do modelo de classificação com melhor desempenho geral (Acurácia, Recall, F1 e ROC AUC).

Visualização das principais métricas e gráficos comparativos via Streamlit.

Entendimento prático do uso do PyCaret para otimização de modelos.

Integração entre automação de ML e experiência interativa.

---

## 🧠 Habilidades Desenvolvidas

✔ Criação e automação de fluxos de Machine Learning
✔ Comparação de modelos com PyCaret
✔ Interpretação e seleção de métricas de performance
✔ Construção de pipeline manual e automatizado
✔ Criação de interfaces analíticas com Streamlit
✔ Documentação técnica e apresentação visual de resultados

---

## 💡 Observação

Este projeto simboliza o fechamento da formação em Ciência de Dados da EBAC, unindo os conceitos teóricos e práticos em uma entrega interativa e reprodutível.
O uso combinado de PyCaret e Streamlit mostra o potencial de automação e comunicação dos resultados de forma acessível e moderna.

📎 Notebook principal: Resultado Projeto Final.ipynb
🖥️ Execução do app interativo:

streamlit run projeto.py

---

✍️ Autora: [Marina França]
🎓 Formação em Ciência de Dados – EBAC
📅 Projeto Final da Trilha de Ciência de Dados
🎬 Vídeo Explicativo: navegacao.mp4