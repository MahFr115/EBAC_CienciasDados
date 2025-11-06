# 📍 Módulo 36 – Regressão Logística II

Nesta segunda etapa da Regressão Logística, o foco deixa de ser apenas a construção do modelo e passa a ser sua **avaliação, interpretação e validação**. A partir das previsões geradas, este módulo mostra como analisar a performance de um modelo de classificação, interpretar probabilidades e otimizar a tomada de decisão baseada em categorias preditas.

Além disso, são apresentados conceitos essenciais para distinguir bons e maus classificadores, como **sensibilidade, especificidade, precisão, F1-score, curva ROC e AUC**.

---

## 🎯 Objetivos do Módulo

✔ Interpretar probabilidades e log-odds preditas pelo modelo  
✔ Construir e analisar a **matriz de confusão**  
✔ Avaliar métricas de desempenho em classificação binária:  
🔹 Acurácia  
🔹 Precisão (Precision)  
🔹 Revocação/Sensibilidade (Recall)  
🔹 Especificidade  
🔹 F1-score  
✔ Ajustar o **limiar (threshold)** de decisão  
✔ Interpretar curvas de probabilidade  
✔ Construir e interpretar a **curva ROC**  
✔ Calcular a **AUC (Área sob a curva ROC)**  
✔ Comparar modelos com base em métricas de performance  
✔ Identificar erros comuns (falsos positivos e falsos negativos)  

---

## 📚 Conteúdo Abordado (com base na prática do módulo)

| Tema | Descrição |
|------|-----------|
| Probabilidade predita | Saída contínua da regressão logística |
| Log-odds | Transformação logarítmica dos odds |
| Threshold | Ponto de corte para definição de classe |
| Matriz de confusão | Distribuição de acertos e erros |
| Acurácia | Proporção de acertos no total |
| Precisão | Proporção de verdadeiros positivos entre os classificados como positivos |
| Recall (Sensibilidade) | Proporção de verdadeiros positivos entre todos os reais positivos |
| Especificidade | Capacidade de evitar falsos positivos |
| F1-score | Média harmônica entre precisão e recall |
| Curva ROC | Relação entre Sensibilidade e 1 - Especificidade |
| AUC | Capacidade discriminante do modelo |

---

## ⚙ Ferramentas Utilizadas

| Ferramenta | Aplicação |
|-----------|-----------|
| `sklearn.linear_model.LogisticRegression` | Modelo base |
| `sklearn.metrics` | Métricas (confusion_matrix, accuracy_score, recall_score, precision_score, f1_score, roc_curve, auc) |
| `matplotlib / seaborn` | Gráficos de curva ROC, matriz de confusão |
| `sklearn.model_selection.train_test_split` | Divisão treino/teste |

---

## 📌 Importância do Módulo

Avaliar a performance de um modelo classificatório é tão importante quanto construí-lo. Este módulo ensina a:

✅ Entender a qualidade das previsões  
✅ Identificar impactos de erros em contextos de negócio (ex: fraude, saúde, crédito)  
✅ Ajustar modelos para balancear entre precisão e recall conforme a necessidade  
✅ Comunicar resultados com métricas compreensíveis  
✅ Escolher de forma precisa o melhor modelo para cada cenário  
