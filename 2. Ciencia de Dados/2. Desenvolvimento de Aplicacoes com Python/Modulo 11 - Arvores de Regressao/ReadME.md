# 🌲 Módulo 11 – Árvores de Regressão

Neste módulo, exploramos a aplicação de **árvores de decisão no contexto de problemas de regressão**, ou seja, quando o objetivo é prever uma **variável contínua**. Assim como nas árvores de classificação, a estrutura do modelo baseia-se em quebras sucessivas dos dados, buscando minimizar o erro dentro de cada região resultante.

Esse módulo aprofunda o entendimento da estrutura, dos critérios de divisão e das técnicas de ajuste e poda para garantir que o modelo seja preciso e tenha boa capacidade de generalização.

---

## 🎯 Objetivos do Módulo

✔ Entender o que são árvores de regressão e como diferem das árvores de classificação  
✔ Compreender os conceitos de **variável explicativa (X)** e **variável resposta (y)**  
✔ Aprender a identificar os melhores pontos de quebra para reduzir o erro  
✔ Utilizar métricas como **MSE, MAE e R²** para avaliar o desempenho do modelo  
✔ Ajustar uma árvore de regressão usando bibliotecas como Scikit-learn  
✔ Aplicar técnicas de **pré-poda e pós-poda** para evitar overfitting  
✔ Conhecer extensões do modelo como **Random Forests e Gradient Boosting**  

---

## 🧩 Principais Conceitos Abordados

| Conceito | Descrição |
|----------|----------|
| **Árvore de Regressão** | Modelo que prevê valores numéricos contínuos |
| **Impureza / Erro** | Medida utilizada para determinar a qualidade das divisões |
| **MSE (Erro Quadrático Médio)** | Mede o erro elevando ao quadrado a diferença entre predição e valor real |
| **MAE (Erro Absoluto Médio)** | Mede o erro pela média dos valores absolutos das diferenças |
| **R² (Coeficiente de Determinação)** | Mede o quanto a variação da variável resposta é explicada pelo modelo |
| **Quebra (Split)** | Ponto em que os dados são divididos para reduzir o erro |
| **Profundidade Máxima** | Limite de níveis para controlar complexidade |
| **Pré-poda** | Impede que a árvore cresça além de um limite |
| **Pós-poda** | A árvore cresce por completo e depois é simplificada |
| **Custo de Complexidade (α / C_p)** | Parâmetro para controlar a poda |
| **Ruído** | Variabilidade aleatória que não deve ser aprendida |
| **Variabilidade** | Grau de dispersão dos dados |
| **Random Forest / Gradient Boosting** | Métodos baseados em múltiplas árvores para melhorar desempenho |

---

## 📑 Glossário

Todos os termos técnicos apresentados neste módulo estão organizados no arquivo **`Glossario.pdf`**, incluindo:  
*MSE, MAE, Impureza, Quebra, Profundidade Máxima, R², Pré-poda, Pós-poda, Parâmetro Alfa, Random Forests, Gradient Boosting, Base de Testes, Base de Treinamento,* entre outros.  
📎 *Local do arquivo: `./Glossario.pdf`* :contentReference[oaicite:0]{index=0}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|------------|
| **Scikit-learn (sklearn)** | Construção, ajuste e poda da árvore |
| **Pandas / NumPy** | Preparação e manipulação dos dados |
| **Jupyter Notebook** | Execução interativa e avaliação do modelo |

---

## 📌 Importância do Módulo

Árvores de Regressão são essenciais para entender como algoritmos supervisionados preditivos operam em variáveis contínuas. Além disso, elas servem como base para técnicas mais poderosas de Machine Learning, como **Random Forests e Gradient Boosting**, amplamente utilizadas no mercado para prever vendas, valores financeiros, consumo energético, entre outros cenários.
