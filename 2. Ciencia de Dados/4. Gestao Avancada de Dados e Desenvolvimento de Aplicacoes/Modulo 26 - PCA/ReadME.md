# 📉 Módulo 26 – PCA (Análise de Componentes Principais)

Este módulo introduz a técnica de **PCA (Principal Component Analysis)**, utilizada para **redução de dimensionalidade** em conjuntos de dados com muitas variáveis. O objetivo é transformar os dados em **novas componentes principais**, preservando o máximo possível da variabilidade original.

O PCA se baseia em conceitos de Álgebra Linear — como **autovalores, autovetores, combinações lineares e projeções** — estudados no **Módulo 25 (Álgebra Linear)**. A técnica é amplamente aplicada em etapas de pré-processamento, visualização e otimização de modelos em Machine Learning.

---

## 🎯 Objetivos do Módulo

✔ Entender a redução de dimensionalidade e quando aplicá-la  
✔ Identificar a **maldição da dimensionalidade** em datasets multivariados  
✔ Criar **componentes principais** como novas variáveis projetadas  
✔ Utilizar autovalores e autovetores para definir eixos de máxima variância  
✔ Avaliar a **variância explicada** por cada componente  
✔ Aplicar critérios como **cotovelo** e **variância mínima explicada** para seleção de componentes  
✔ Implementar PCA com bibliotecas como `sklearn`  
✔ Compreender impactos da redução na performance de modelos  

---

## 📚 Conteúdo Abordado

| Tema | Descrição |
|------|-----------|
| PCA (Análise de Componentes Principais) | Técnica de redução de dimensionalidade |
| Dimensionalidade | Número de variáveis de um conjunto de dados |
| Maldição da dimensionalidade | Perda de desempenho com muitas variáveis |
| Componentes principais | Novas variáveis formadas por combinações lineares |
| Redundância de informação | Correlação alta entre variáveis originais |
| Variabilidade e variância | Dispersão dos dados e explicação de variação |
| Autovalores | Quantidade de variância explicada por cada componente |
| Autovetores | Direções de maior variabilidade dos dados |
| Variância explicada | Percentual de informação retida por componente |
| Critério de variância explicada | Definição de threshold mínimo de retenção |
| Critério do cotovelo | Escolha subjetiva com base em curva de variância |
| Grid Search | Otimização de hiperparâmetros (aplicável quando PCA é parte de pipeline) |
| PCA com sklearn | Implementação prática em Python |

📎 Glossário completo disponível em: **`Glossario.pdf`** :contentReference[oaicite:0]{index=0}

---

## 🛠 Aplicações na Ciência de Dados

| Aplicação | Como o PCA contribui |
|-----------|---------------------|
| Pré-processamento | Reduz ruído e redundância |
| Visualização de dados | Geração de gráficos em 2D/3D a partir de dados multivariados |
| Performance de modelos | Menos variáveis → menor complexidade |
| Combate ao overfitting | Redução de variáveis irrelevantes |
| Pipeline com Scikit-Learn | Componente de transformação integrado ao treinamento |

---

## 📌 Importância do Módulo

O PCA é uma ferramenta essencial para quem trabalha com **dados de alta dimensionalidade**, pois permite simplificar a estrutura do dataset sem comprometer (ou comprometendo minimamente) a quantidade de informação. Dominar PCA é importante não apenas para modelagem, mas também para **compreensão da estrutura dos dados**.