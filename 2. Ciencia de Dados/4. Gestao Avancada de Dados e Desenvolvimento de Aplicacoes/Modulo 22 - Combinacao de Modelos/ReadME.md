# 🤖 Módulo 22 – Combinação de Modelos I

Este módulo marca o início do estudo de **combinação de modelos (ensemble learning)**, uma das abordagens mais eficazes para aumentar a precisão e a robustez dos modelos de Machine Learning. Ele é uma continuação do aprendizado iniciado no **Módulo 16 – Árvores II**, evoluindo de árvores individuais para técnicas que unem diversas árvores para criar previsões mais estáveis.

O foco aqui está no método **Bagging (Bootstrap Aggregating)** e em seu principal representante: **Random Forest**.

---

## 🎯 Objetivos do Módulo

✔ Entender o conceito de **ensemble learning** e por que combinar modelos melhora a performance  
✔ Aprender o método **Bagging**, com base em amostragem com reposição  
✔ Compreender a lógica de votação/média de previsões em ensembles  
✔ Introduzir a **Random Forest**, uma evolução do Bagging aplicada a Árvores  
✔ Identificar como ensembles reduzem **overfitting** e aumentam generalização  
✔ Ajustar **hiperparâmetros da Random Forest**  
✔ Utilizar técnicas de busca como **Grid Search (GridSearchCV)**  
✔ Avaliar o modelo com métricas como **Curva ROC, KS e Gini**  

---

## 📚 Conteúdo Abordado

| Tema | Descrição |
|------|-----------|
| Ensemble Learning | Combinação de múltiplos modelos para melhor previsão |
| Bagging | Método baseado em múltiplas amostras aleatórias com reposição |
| Bootstrap | Processo de reamostragem utilizado no Bagging |
| Agregação | Votação (classificação) ou média (regressão) de previsões |
| Random Forest | Conjunto de árvores com variáveis aleatórias em cada divisão |
| Overfitting | Erros por excesso de ajuste em um único modelo |
| Hiperparâmetros | Controles do modelo (n_estimators, max_depth, etc.) |
| Tunning | Processo de ajuste fino dos hiperparâmetros |
| GridSearchCV | Busca automática por melhores parâmetros em grade |
| Curva ROC | Avaliação probabilística de modelos de classificação |
| Gini | Métrica derivada da curva ROC |
| KS | Medida de separação entre distribuições previstas |

---

## 📑 Glossário do Módulo

O glossário completo com os conceitos abordados está presente em:  
📎 **`./Glossario.pdf`** :contentReference[oaicite:0]{index=0}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|-----------|
| **Scikit-Learn** | Implementação de Random Forest e GridSearchCV |
| **Pandas / NumPy** | Preparação de dados |
| **Matplotlib / Seaborn** | Visualização de métricas como curva ROC |
| **Jupyter Notebook** | Teste e ajuste iterativo do modelo |

---

## 📌 Importância do Módulo

O Bagging e a Random Forest são amplamente utilizados em aplicações reais devido à sua capacidade de:

✅ Melhorar a precisão preditiva  
✅ Reduzir overfitting em comparação a modelos simples  
✅ Oferecer interpretações por importância de variáveis  
✅ Servir como base para evoluções futuras como Boosting e Gradient Boosting  