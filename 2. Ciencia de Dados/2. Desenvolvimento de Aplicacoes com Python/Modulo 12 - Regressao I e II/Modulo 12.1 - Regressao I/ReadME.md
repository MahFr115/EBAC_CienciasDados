# 📉 Regressão I: Fundamentos e Estimação do Modelo

Este módulo marca a entrada nos modelos de **regressão linear**, uma técnica amplamente utilizada para prever variáveis contínuas com base em uma ou mais variáveis explicativas. Aqui são introduzidos os componentes matemáticos do modelo e o processo de estimar os coeficientes de regressão utilizando o método dos mínimos quadrados.

---

## 🎯 Objetivos do Módulo

✔ Compreender a equação de regressão linear simples  
✔ Entender os papéis de **alfa (α)**, **beta (β)** e do termo de erro (**ε**)  
✔ Identificar variável dependente (Y) e variável independente (X)  
✔ Introduzir a biblioteca **statsmodels** para ajuste de modelos  
✔ Estimar coeficientes por meio do **método de Mínimos Quadrados (OLS)**  
✔ Avaliar a qualidade inicial do ajuste do modelo  

---

## 📐 Conceitos Fundamentais

| Conceito | Descrição |
|----------|-----------|
| **α (Alfa)** | Intercepto: valor previsto de Y quando X = 0 |
| **β (Beta)** | Inclinação: variação esperada em Y para cada unidade em X |
| **ε (Epsilon)** | Erro aleatório não explicado pelo modelo |
| **Variável Dependente (Y)** | Valor que se deseja prever |
| **Variável Independente (X)** | Variável usada para prever Y |
| **Sigma² (σ²)** | Variância dos erros |
| **OLS – Ordinary Least Squares** | Método usado para estimar os coeficientes minimizando os resíduos |

---

## 🧪 Estimação do Modelo com Statsmodels

No statsmodels, utiliza-se a função `OLS()` para criar o modelo e métodos como `.fit()` para estimá-lo. São apresentados recursos como:

✔ Objeto `reg`  
✔ Método `predict` para previsões  
✔ Intervalos de confiança dos parâmetros  

---

## ⚠ Erro e Avaliação Inicial

| Métrica | O que representa |
|---------|------------------|
| **Erro Quadrado Médio (MSE)** | Diferença média ao quadrado entre valores estimados e reais |
| **Valor Observado vs Valor Previsto** | Avaliação pontual do modelo |

---

## 📑 Glossário

Este módulo utiliza os conceitos apresentados no arquivo **`Glossario.pdf`**, incluindo termos como: `Alfa`, `Beta`, `Epsilon`, `OLS`, `Intercepto`, `Erro Quadrado Médio`, `Intervalo de Confiança`, `predict`, entre outros.  
📎 *Local do arquivo: `./Glossario.pdf`*

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|------------|
| **Statsmodels** | Ajuste e avaliação de modelos de regressão |
| **Pandas / NumPy** | Estruturação e manipulação de dados |
| **Jupyter Notebook** | Execução e análise interativa |

---

## 📌 Importância do Módulo

O aprendizado da Regressão Linear é um dos pilares da modelagem preditiva. Dominar sua equação, parâmetros e método de ajuste é essencial para avançar para modelos mais complexos e para compreender variações como regressão múltipla, regularização, árvores de regressão e redes neurais.