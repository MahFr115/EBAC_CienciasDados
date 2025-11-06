# 📊 Módulo 9 – Agregação e Operações em Grupos com Pandas

Este módulo aprofunda o uso do Pandas no contexto de **análise descritiva avançada**, explorando técnicas de **agregação, agrupamento e sumarização de dados**. A partir das funções `groupby()`, `apply()` e `pivot_table()`, aprendemos a transformar grandes conjuntos de dados em informações estruturadas e relevantes para tomada de decisão.

---

## 🎯 Objetivos do Módulo

✔ Entender o conceito de agregação de dados e sua utilidade na análise  
✔ Aplicar o método `groupby()` para dividir dados em grupos com base em critérios definidos  
✔ Utilizar funções estatísticas (como `sum`, `mean`, `count`, etc.) para resumir grupos  
✔ Explorar o método `apply()` para aplicar funções personalizadas a cada grupo  
✔ Criar tabelas dinâmicas com `pivot_table()`  
✔ Utilizar funções de categorização como `cut()` e `qcut()`  
✔ Consolidar insights a partir de segmentações de dados  

---

## 📂 Conteúdo Abordado

| Tema | Descrição |
|------|-----------|
| Conceito de agregação | Consolidação de múltiplos valores em um único resultado |
| `groupby()` | Agrupa dados com base em colunas específicas |
| `apply()` | Aplica funções personalizadas por grupo |
| Função `top` (exemplo) | Seleção de n maiores valores por grupo |
| Função `cut()` | Segmentação de variáveis contínuas em categorias fixas |
| Função `qcut()` | Categorização baseada em quantis |
| `pivot_table()` | Criação de tabelas dinâmicas para sumarização |
| `margins=True` | Adição de totais na tabela pivô |

---

## 📑 Glossário de Conceitos

Todos os termos centrais trabalhados neste módulo estão explicados no arquivo **`Glossario.pdf`**, como:  
✔ `Agregação`  
✔ `GroupBy`  
✔ `Apply`  
✔ `Top`  
✔ `cut()`  
✔ `qcut()`  
✔ `pivot_table()`  
✔ `margins`

📎 *Local do arquivo: `./Glossario.pdf`*

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|------------|
| **Pandas** | Agrupamento, agregação e geração de tabelas analíticas |
| **NumPy** | Suporte matemático para funções aplicadas em agregações |
| **Jupyter Notebook** | Execução interativa dos exemplos |

---

## 📌 Importância deste módulo

A habilidade de realizar **agregações e operações por grupo é fundamental em qualquer análise de dados**, permitindo responder perguntas como: _“Qual categoria tem maior média?”_ ou _“Quais os segmentos mais relevantes por região?”_. Essas técnicas são amplamente aplicadas em relatórios gerenciais, dashboards, análises de comportamento e preparação para modelagem preditiva.