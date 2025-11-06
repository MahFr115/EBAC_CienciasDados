# 🚀 Módulo 23 – Combinação de Modelos II

Dando continuidade ao estudo de **técnicas de combinação de modelos (ensemble learning)** iniciado no **Módulo 22 (Bagging & Random Forest)**, este módulo apresenta o método de **Boosting**, uma estratégia poderosa que combina modelos fracos de forma sequencial para criar um preditor altamente robusto e preciso.

Ao contrário do Bagging, onde os modelos são treinados de forma independente, o **Boosting constrói modelos de forma sequencial**, dando mais peso aos erros cometidos pelos modelos anteriores.

---

## 🎯 Objetivos do Módulo

✔ Entender os fundamentos do **Boosting**  
✔ Comparar **Bagging x Boosting**  
✔ Conhecer o funcionamento do **AdaBoost** (Adaptive Boosting)  
✔ Aprender o conceito de **resíduos como sinal de ajuste incremental**  
✔ Compreender a ideia de **função de perda e gradiente**  
✔ Explorar o **Gradient Boosting Machine (GBM)**  
✔ Conhecer o **Stochastic Gradient Boosting** e o uso de subamostragem  
✔ Introduzir o **XGBoost**, otimizado com paralelismo e regularização  
✔ Avaliar modelos com métricas como **ROC AUC** e validação fora do tempo  
✔ Ajustar hiperparâmetros e compreender critérios de parada  

---

## 📚 Conteúdo Abordado

| Tema | Descrição |
|------|-----------|
| Boosting | Treinamento sequencial de modelos fracos |
| AdaBoost | Ajuste progressivo baseado na correção de erros |
| Função de Perda | Mede o erro entre previsto e real |
| Resíduos | Erros que guiam o aprendizado das próximas árvores |
| GBM (Gradient Boosting Machine) | Boosting guiado por gradiente da perda |
| Stochastic Gradient Boosting | Uso de subamostragem para melhorar generalização |
| XGBoost | Implementação otimizada com paralelismo, regularização e eficiência |
| Robustez | Capacidade de evitar overfitting |
| Critério de Parada | Número de iterações/árvores ou convergência da perda |
| Validação Fora do Tempo | Método de validação temporal |
| Validação com troca | Alternância de períodos para avaliar estabilidade |
| ROC AUC | Métrica de separação entre classes |
| Impacto relativo das variáveis | Interpretação da importância das features |

---

## 📑 Glossário do Módulo

Os conceitos apresentados estão detalhados no arquivo:  
📎 **`Glossario.pdf`** :contentReference[oaicite:0]{index=0}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|-----------|
| **Scikit-Learn (AdaBoostClassifier, GradientBoostingClassifier)** | Construção de modelos Boosting |
| **XGBoost** | Versão otimizada do GBM |
| **Pandas / NumPy** | Preparação de dados |
| **Matplotlib / Seaborn** | Visualização de métricas como ROC |
| **GridSearchCV / RandomizedSearchCV** | Ajuste de hiperparâmetros |

---

## 📌 Importância do Módulo

O Boosting é uma das técnicas mais utilizadas em competições e aplicações reais por oferecer:

✅ Alta performance preditiva  
✅ Correção iterativa de erros  
✅ Maior capacidade de ajuste que uma árvore individual  
✅ Menor tendência a overfitting quando bem configurado  
✅ Modelos de referência como XGBoost dominam desafios reais de Machine Learning  