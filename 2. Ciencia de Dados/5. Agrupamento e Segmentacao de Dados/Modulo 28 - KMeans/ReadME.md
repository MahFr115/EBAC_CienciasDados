# 📍 Módulo 28 – K-means (Clusterização Não Supervisionada)

Este módulo introduz o **K-means**, um dos algoritmos mais utilizados em **aprendizado de máquina não supervisionado**, com foco em agrupar dados semelhantes em grupos chamados **clusters**. A técnica é amplamente aplicada em segmentação de clientes, detecção de padrões, compressão de dados e insights exploratórios.

O K-means baseia-se na ideia de minimizar a distância entre os pontos e o centro de seu grupo, o **centróide**, atualizando iterativamente esses centros até atingir a convergência.

---

## 🎯 Objetivos do Módulo

✔ Compreender os fundamentos do algoritmo K-means  
✔ Aprender o conceito de distância Euclidiana  
✔ Identificar o papel dos centróides e sua atualização  
✔ Entender parâmetros iniciais e seu impacto no resultado  
✔ Reconhecer o critério de convergência do algoritmo  
✔ Avaliar a qualidade do agrupamento com o método da silhueta  
✔ Calcular a soma dos quadrados das distâncias (inércia)  
✔ Aplicar K-means em tarefas de clusterização com Python  

---

## 📚 Conteúdo Abordado

| Tema | Descrição |
|------|-----------|
| Algoritmo K-means | Agrupa dados em K clusters com base em similaridade |
| Cluster | Grupo de pontos similares determinado pela distância ao centróide |
| Distância Euclidiana | Métrica que mede a proximidade entre pontos |
| Função “standard” | Padroniza variáveis (média zero, desvio padrão 1) |
| Pontos de dados | Observações que serão agrupadas |
| Centróides | Pontos centrais de cada cluster (média dos pontos) |
| Parâmetros iniciais | Número de clusters e posição inicial dos centróides |
| Convergência | Quando os centróides não mudam mais entre iterações |
| Soma dos Quadrados da Distância (inércia) | Mede o ajuste do cluster |
| Método da Silhueta | Avalia a qualidade dos agrupamentos |
| Determinação do número de clusters | Uso de critérios como silhueta e inércia |

📎 Glossário completo disponível em: **`Glossario.pdf`** :contentReference[oaicite:1]{index=1}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|-----------|
| **Scikit-Learn (KMeans)** | Implementação do algoritmo |
| **Pandas / NumPy** | Manipulação de dados |
| **Matplotlib / Seaborn** | Visualização de clusters |
| **StandardScaler** | Padronização prévia dos dados |

---

## 📌 Importância do Módulo

O K-means é frequentemente o primeiro passo em tarefas de **análise exploratória avançada**, ajudando na compreensão da estrutura interna dos dados ao revelar **padrões ocultos e agrupamentos naturais**. O entendimento deste algoritmo é fundamental para o aprendizado de outras técnicas de clusterização e segmentação.