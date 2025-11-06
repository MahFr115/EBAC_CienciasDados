# 🌳 Módulo 7 – Árvores de Decisão (Parte 1)

Este módulo introduz o primeiro algoritmo de **aprendizado de máquina supervisionado** estudado no curso: as **Árvores de Decisão**, amplamente utilizadas pela sua facilidade de interpretação e capacidade de solucionar problemas de **classificação e regressão**. A partir deste ponto, entramos oficialmente no universo de modelagem preditiva em Ciência de Dados.

---

## 🎯 Objetivos do Módulo

✔ Entender o funcionamento das Árvores de Decisão  
✔ Diferenciar árvores para **classificação** e **regressão**  
✔ Compreender a estrutura de uma árvore: nó raiz, nós internos, ramos e folhas  
✔ Calcular critérios de divisão e selecionar a melhor variável e ponto de corte  
✔ Trabalhar com variáveis explicativas (X) e alvo (y)  
✔ Ajustar modelos utilizando a biblioteca **Scikit-learn**  
✔ Realizar técnicas de **poda** para evitar overfitting  
✔ Conhecer vantagens, limitações e variações como Random Forest e XGBoost  

---

## 🧠 Estrutura conceitual da árvore

| Elemento | Descrição |
|---------|-----------|
| **Nó raiz** | Primeiro ponto de decisão da árvore |
| **Nós internos** | Pontos de quebra ao longo do aprendizado |
| **Ramos** | Caminhos que conectam os nós |
| **Folhas** | Resultado final (classe ou valor predito) |
| **Profundidade** | Nível de camadas da árvore |

---

## 📊 Processo de construção da árvore

1. Carregar e preparar os dados  
2. Definir variáveis **explicativas (X)** e **alvo (y)**  
3. Avaliar possíveis pontos de corte  
4. Escolher o critério de divisão (ex: **Impureza de Gini**)  
5. Crescer a árvore  
6. Aplicar **poda** (pruning) para reduzir complexidade  
7. Avaliar prós e contras  

---

## 📐 Critérios e parâmetros importantes

| Conceito | Função |
|----------|--------|
| **Impureza de Gini** | Mede a pureza dos nós (quanto menor, melhor) |
| **C Alfa (α)** | Parâmetro de complexidade usado na poda |
| **Ponto de corte** | Valor de divisão escolhido para separar dados |
| **Scikit-learn** | Biblioteca utilizada para implementação |

---

##✂️ Poda (Pruning)

✔ Evita overfitting  
✔ Utiliza o parâmetro `C alfa` e métodos como `'complex'`  
✔ Pós-poda: a árvore cresce e depois é reduzida ao ideal  

---

## ⚖️ Vantagens e desvantagens

| Prós | Contras |
|------|--------|
| Modelo de **caixa branca** (interpretável) | Pode sofrer **overfitting** |
| Funciona com variáveis categóricas e numéricas | Divisões podem ficar enviesadas |
| Suporta múltiplas saídas | Pode exigir poda para eficiência |

---

## 📚 Glossário

O arquivo **`Glossario.pdf`** contém todos os termos principais apresentados neste módulo, como:  
`Árvore de Classificação`, `Árvore de Regressão`, `Gini`, `C Alfa`, `Random Forest`, `XGBoost`, `Profundidade`, `Folha`, `Ponto de Corte`, `Classificador (clf)`, entre outros.  
📎 *Local do arquivo: `./Glossario.pdf`*

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|------------|
| **Scikit-learn (sklearn)** | Construção e poda da árvore |
| **Pandas / NumPy** | Estruturação dos dados |
| **Jupyter Notebook** | Treinamento interativo do modelo |

---

## 📌 Importância deste módulo

As Árvores de Decisão são uma base essencial para compreender outras técnicas de Machine Learning, incluindo algoritmos de conjunto como **Random Forest** e **XGBoost**, muito utilizados no mercado por sua alta performance. Dominar esse modelo é o primeiro passo rumo ao aprendizado aprofundado de algoritmos supervisionados.
