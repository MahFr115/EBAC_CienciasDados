# 📉 Módulo 12 – Regressão Linear: Parte I e Parte II

Este módulo apresenta a **Regressão Linear**, um dos modelos estatísticos e preditivos mais utilizados em Ciência de Dados para prever valores contínuos. O conteúdo está dividido em duas partes: a primeira foca na compreensão do modelo e estimativa de parâmetros; a segunda aborda avaliação, diagnóstico e interpretação dos resultados.

---

## 📍 Estrutura do Módulo

| Parte | Foco Principal |
|-------|----------------|
| **Regressão I** | Construção do modelo, interpretação da equação e estimação dos parâmetros |
| **Regressão II** | Avaliação estatística, verificação de ajuste e métricas de desempenho |

---

## 📘 Parte I – Fundamentos e Estimação do Modelo

### 🎯 Objetivos

✔ Compreender a equação da regressão linear simples  
✔ Identificar os componentes: **α (alfa), β (beta) e ε (erro)**  
✔ Distinguir variáveis dependentes (Y) e independentes (X)  
✔ Estimar os parâmetros usando o método de **Mínimos Quadrados (OLS)**  
✔ Utilizar a biblioteca `statsmodels` para ajuste do modelo  
✔ Fazer previsões com o modelo ajustado  

### 📐 Equação do Modelo

\[
Y = \alpha + \beta X + \varepsilon
\]

| Componente | Significado |
|------------|-------------|
| **α (alfa)** | Intercepto – valor de Y quando X = 0 |
| **β (beta)** | Inclinação – variação de Y para cada unidade em X |
| **ε (epsilon)** | Erro aleatório |
| **σ² (sigma²)** | Variância dos erros |

---

## 📘 Parte II – Avaliação do Modelo e Diagnóstico

### 🎯 Objetivos

✔ Avaliar a qualidade do ajuste do modelo  
✔ Analisar a significância dos coeficientes  
✔ Verificar a adequação por meio de métricas como **R², MSE e MAE**  
✔ Entender a variabilidade explicada e resíduos  
✔ Realizar previsões e intervalos de confiança  
✔ Discutir hipóteses do modelo e possíveis erros  

### 📊 Métricas de Avaliação

| Métrica | Interpretação |
|---------|--------------|
| **MSE (Erro Quadrático Médio)** | Mede o erro médio ao quadrado |
| **MAE (Erro Absoluto Médio)** | Média dos erros absolutos entre previsto e observado |
| **R² (Coeficiente de Determinação)** | Percentual da variabilidade explicada pelo modelo |

---

## 📑 Glossário

Todos os conceitos apresentados neste módulo estão detalhados no arquivo **`Glossario.pdf`**, incluindo:  
✔ Alfa (α), Beta (β), Epsilon (ε), Sigma²  
✔ Mínimos Quadrados (OLS), Erro Quadrático Médio, R²  
✔ Variável Dependente x Independente  
✔ `predict`, Intervalos de Confiança  
✔ Soma dos Quadrados dos Resíduos, Coeficiente de Determinação  

📎 *Local do arquivo: `./Glossario.pdf`*

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|------------|
| **Statsmodels** | Ajuste e extração de métricas do modelo |
| **Scikit-learn (opcional)** | Alternativa prática para regressão |
| **Pandas / NumPy** | Manipulação e preparação dos dados |
| **Jupyter Notebook** | Execução e análise dos modelos |

---

## 📌 Importância do Módulo

A Regressão Linear é base para diversos modelos mais avançados, como Regressão Múltipla, Ridge, Lasso, ElasticNet e Regressão Logística. Além disso, sua interpretação clara é essencial para que cientistas de dados compreendam os impactos das variáveis no comportamento da resposta.