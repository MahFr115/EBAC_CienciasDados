# 📊 Módulo 29 – Clusterização Hierárquica e Aglomerativa

Dando continuidade ao estudo de técnicas de **aprendizado não supervisionado**, este módulo apresenta os métodos de **agrupamento hierárquico**, com ênfase no modelo **aglomerativo**, uma abordagem que cria clusters progressivamente, unindo observações com base em sua similaridade.

Diferente do **K-means (Módulo 28)**, que exige a definição prévia do número de clusters, a clusterização hierárquica permite explorar diferentes níveis de agrupamento e visualizar as formações de clusters por meio de um **dendrograma**, o que facilita a análise exploratória.

---

## 🎯 Objetivos do Módulo

✔ Entender o conceito de agrupamento hierárquico  
✔ Diferenciar clusterização aglomerativa (bottom-up) e divisiva (top-down)  
✔ Compreender como ocorre a união sucessiva de pontos em grupos  
✔ Utilizar diferentes critérios de **ligação (linkage)** para combinar clusters  
✔ Trabalhar com matrizes de distância  
✔ Avaliar formas de medir similaridade entre dados quantitativos e mistos  
✔ Visualizar resultados com **dendrogramas**  
✔ Aplicar o método para determinar número ideal de clusters  

---

## 📚 Conteúdo Abordado

| Tema | Descrição |
|------|-----------|
| Algoritmos não supervisionados | Classificação de métodos sem variáveis resposta |
| Agrupamento hierárquico | Construção progressiva de clusters |
| Aglomerativo (bottom-up) | Cada ponto inicia como cluster individual e se unem |
| Divisivo (top-down) | Parte de um cluster único e divide progressivamente |
| Ligação (Linkage) | Critério de conexão entre clusters |
| Tipos de ligação | Simples, completa, média, Ward |
| Matriz de distâncias | Distâncias entre pares de observações |
| Distância Euclidiana | Usual para dados quantitativos |
| Distância Manhattan | Baseada em deslocamentos horizontais e verticais |
| Distância Dice | Ideal para dados categóricos |
| Distância Gower | Indicada para dados mistos |
| Dendrograma | Representação gráfica da hierarquia de agrupamentos |
| Ponto de quebra | Local no dendrograma para corte dos clusters |
| Centroide | Ponto médio do grupo (em variação de clusterização) |

📎 Glossário completo disponível em: **`Profissão Cientista de Dados M30 Glossário.pptx`** :contentReference[oaicite:1]{index=1}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Uso |
|-----------|-----|
| **Scikit-Learn (`AgglomerativeClustering`)** | Implementação da clusterização aglomerativa |
| **SciPy (`linkage`, `dendrogram`)** | Geração de matrizes de ligação e dendrogramas |
| **Pandas / NumPy** | Pré-processamento de dados |
| **Distance (spal)** | Cálculo de distâncias específicas |
| **Matplotlib / Seaborn** | Visualização de dendrogramas |

---

## 📌 Importância do Módulo

Este método é amplamente utilizado quando se busca **compreender a estrutura de agrupamento natural de dados**, especialmente em análises exploratórias. A clusterização hierárquica é especialmente útil quando não se conhece previamente o número de clusters e quando é necessário comparar diferentes níveis de granularidade dos grupos.

✅ Após este módulo, o aluno será capaz de escolher entre técnicas como **K-means ou clusterização hierárquica**, conforme a natureza dos dados e os objetivos da análise.