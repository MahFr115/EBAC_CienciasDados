# 🛢️ Módulo 20 – PostgreSQL

Este módulo introduz o uso do **PostgreSQL**, um dos principais SGBDs (Sistemas de Gerenciamento de Banco de Dados Relacionais) utilizados no mercado, e apresenta como conectar o Python ao banco utilizando a biblioteca **psycopg2**. Para fins práticos, é utilizado o dataset `dvdrental` como exemplo de exploração e consultas.

---

## 🎯 Objetivos do Módulo

✔ Entender o que é PostgreSQL e sua importância na Ciência de Dados  
✔ Configurar e acessar bancos utilizando **PGAdmin**  
✔ Compreender o papel de um **SGBD (Sistema de Gerenciamento de Banco de Dados)**  
✔ Introduzir a linguagem **SQL** e conceitos de consultas  
✔ Estabelecer conexão entre Python e PostgreSQL com `psycopg2`  
✔ Ler dados de tabelas e transformá-los em um **DataFrame do Pandas**  
✔ Executar consultas com agregações, junções e ordenação  
✔ Explorar conceitos como tabelas intermediárias, código de-para e visualização de dados  

---

## 📚 Conteúdo Abordado

| Tema | Descrição |
|------|-----------|
| PostgreSQL | Banco de dados relacional open-source para cargas complexas |
| PGAdmin | Ferramenta gráfica de administração do PostgreSQL |
| SGBD | Sistema que gerencia a criação, leitura, atualização e exclusão de dados |
| SQL | Linguagem para manipulação e consulta de dados estruturados |
| psycopg2 | Biblioteca Python para conexão com PostgreSQL |
| `desc.name` | Recurso utilizado para recuperar os nomes das colunas retornadas |
| Pandas DataFrame | Estrutura de dados para manipulação tabular após leitura do BD |
| Agregação | Uso de funções SQL como `SUM`, `AVG`, `MAX`, `MIN`, `COUNT` |
| Código de-para | Relação entre códigos e suas descrições categóricas |
| Cruzamento/Junção de tabelas | Combinação de dados com `INNER JOIN`, `LEFT JOIN`, etc. |
| Ordenação de resultados | Uso de `ORDER BY` para classificar os dados |
| Tabela intermediária | Utilizada para representar relações muitos-para-muitos |
| Visualização de tabelas | Comando `SELECT` para leitura de dados |

---

## 📑 Glossário do Módulo

O glossário completo dos termos apresentados pode ser encontrado em:  
📎 **`./Glossario.pdf`** :contentReference[oaicite:1]{index=1}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|-----------|
| **PostgreSQL** | Armazenamento e gerenciamento de dados relacionais |
| **PGAdmin** | Interface gráfica para consulta e administração de bases |
| **Python (psycopg2)** | Conexão e extração programática de dados |
| **Pandas** | Conversão de dados SQL em DataFrames para análise |
| **SQL** | Criação e execução de consultas |

---

## 📌 Importância do Módulo

O domínio de bancos de dados relacionais é essencial na rotina de um cientista de dados, pois a maioria dos dados corporativos está armazenada em SGBDs como o PostgreSQL. Conectar Python ao banco permite a criação de pipelines analíticos eficientes, integrando os dados diretamente ao fluxo de análise, modelagem e visualização.
