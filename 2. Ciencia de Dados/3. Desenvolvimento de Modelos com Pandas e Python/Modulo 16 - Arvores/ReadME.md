# 🌳 Módulo 16 – Árvores II

Este módulo dá continuidade ao conteúdo introduzido no **Módulo 8 – Árvores de Decisão**, avançando para temas mais complexos como **classificação multinomial, impureza, overfitting, poda e validação cruzada**, essenciais para construção de modelos de árvore mais robustos e interpretáveis.

---

## 🎯 Objetivos do Módulo

✔ Compreender a diferença entre **classificação binária e multinomial**  
✔ Explorar **métricas de impureza** (Entropia e Gini)  
✔ Identificar e corrigir **overfitting em árvores**  
✔ Entender o **custo de complexidade** e como ele se relaciona com a poda  
✔ Realizar **poda de árvores** para generalização  
✔ Conhecer e aplicar **validação cruzada (Cross Validation)**  
✔ Trabalhar com **hiperparâmetros** na otimização do modelo  

---

## 📚 Conteúdo Abordado

| Tema | Descrição |
|------|-----------|
| Classificação Binária vs Multinomial | Diferenças entre modelos com duas ou mais classes |
| Impureza | Medida usada para avaliar a “mistura” de classes em um nó |
| Entropia | Métrica baseada na teoria da informação |
| Gini | Critério alternativo para medir impureza |
| Construção de árvores multinomiais | Extensão das árvores para múltiplas classes |
| Overfitting | Quando a árvore se ajusta demais aos dados de treino |
| Custo de complexidade | Penalização do crescimento excessivo da árvore |
| Poda | Redução do tamanho do modelo para evitar overfitting |
| Validação Cruzada (Cross-validation) | Uso de subconjuntos para validar desempenho |
| Tipos de validação | k-fold, leave-one-out, exaustiva, não exaustiva, hierárquica |
| Hiperparâmetros | Parâmetros de controle da árvore (profundidade, min_samples_split, etc.) |

---

## 📑 Glossário do Módulo

O arquivo **`Glossario.pdf`** aborda termos cruciais como:  
🔹 Classificação binária • Classificação multinomial • Impureza  
🔹 Entropia • Gini • Custo de complexidade • Poda  
🔹 Overfitting • Cross-validation • Hiperparâmetros  
📎 *Local do arquivo: `./Glossario.pdf`* :contentReference[oaicite:0]{index=0}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|-----------|
| **Scikit-Learn** | Construção e poda de árvores |
| **Python (Pandas/Numpy)** | Manipulação de dados |
| **Jupyter Notebook** | Testes e análise interativa |

---

## 📌 Importância do Módulo

Ao dominar esses conceitos, o aluno passa a entender como prevenir modelos frágeis ou superajustados, preparando-se para o tuning de modelos mais complexos e para validações rigorosas em ambientes reais.