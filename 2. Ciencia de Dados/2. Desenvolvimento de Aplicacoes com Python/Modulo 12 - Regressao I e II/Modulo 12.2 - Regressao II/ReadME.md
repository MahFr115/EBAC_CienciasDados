# 📊 Regressão II – Avaliação, Inferência e Seleção de Modelos

Esta segunda etapa do módulo de Regressão aprofunda os conceitos iniciados em Regressão I, ampliando a análise do modelo para além do ajuste inicial. Aqui, o foco está em entender a capacidade de explicação do modelo, avaliar sua qualidade estatística, tomar decisões sobre complexidade e selecionar a melhor configuração para previsão.

---

## 🎯 Objetivos da Etapa

✔ Diferenciar **previsão** de **explicação estatística**  
✔ Realizar **inferência sobre parâmetros** do modelo  
✔ Compreender métricas de qualidade do ajuste como **R² e AIC**  
✔ Discutir a relação entre **complexidade e overfitting**  
✔ Entender o conceito de **correlação espúria**  
✔ Aplicar métodos de **seleção de modelos** (forward, backward, stepwise)  
✔ Introduzir técnicas de **regularização** (Ridge, Lasso, Elastic Net)  

---

## 📘 Conteúdos Abordados

| Tema | Descrição |
|------|-----------|
| Previsão vs Explicação | Modelos preditivos vs modelos interpretativos |
| Inferência estatística | Hipóteses sobre parâmetros, valor-p e intervalos de confiança |
| Qualidade vs Complexidade | Equilíbrio entre ajuste e generalização |
| Critérios de seleção | AIC, R², erro mínimo, princípio da Navalha de Occam |
| Overfitting | Quando o modelo memoriza em vez de generalizar |
| Correlação espúria | Associações falsas causadas por variáveis ocultas |
| Métodos de Seleção de Variáveis | Forward Selection, Backward Elimination e Stepwise |
| Regularização | Penalização de coeficientes para reduzir complexidade |
| Elastic Net | Combinação das penalizações L1 (Lasso) e L2 (Ridge) |

---

## 📑 Glossário desta Etapa

Os seguintes termos são detalhados no arquivo **`Profissao Cientista de Dados M13 Glossario.pdf`**:

✅ Previsão • Explicação • Redução de erro  
✅ Intervalo de confiança • Valor p • Variância homogênea  
✅ AIC • Correlação espúria • Mínimos quadrados • Overfitting  
✅ Navalha de Occam • R Quadrado (R²)  
✅ Forward Selection • Backward Elimination • Stepwise  
✅ Regularização • Elastic Net • Estimador de mínimos quadrados

📎 *Local do arquivo: `./Profissao Cientista de Dados M13 Glossario.pdf`* :contentReference[oaicite:1]{index=1}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Aplicação |
|-----------|-----------|
| **Statsmodels** | Extração de parâmetros, intervalos de confiança e valor-p |
| **Scikit-learn** | Implementação de regressões com regularização (Lasso, Ridge, Elastic Net) |
| **Pandas / NumPy** | Manipulação dos dados |
| **Jupyter Notebook** | Experimentação e análise interpretativa |

---

## 📌 Importância desta etapa

A compreensão da etapa analítica e inferencial da regressão permite que o cientista de dados:

✅ Justifique estatisticamente os parâmetros  
✅ Entenda a relevância de cada variável  
✅ Saiba prevenir modelos com ajuste ilusório  
✅ Aprenda a escolher o melhor modelo com base em critérios técnicos  
✅ Construa modelos robustos e generalizáveis  