# 🧮 Projeto SQL para Análise de Dados – EBAC

Este projeto foi desenvolvido como parte da formação em **Ciência de Dados da EBAC**, na trilha de **SQL para Análise de Dados**.  
O objetivo foi realizar consultas analíticas em uma base de dados de clientes de cartão de crédito, hospedada em **AWS S3** e consultada via **AWS Athena**, para extrair insights sobre perfil, comportamento e padrões de consumo.

Os resultados foram visualizados por meio de **gráficos no Power BI** e documentados em um ambiente **Google Colab**.

---

## 🎯 Objetivos do Projeto

✔ Criar uma base relacional em nuvem e executar consultas SQL para análise exploratória  
✔ Compreender a estrutura e comportamento das variáveis de uma base de clientes  
✔ Identificar padrões de comportamento, perfis de risco e insights de negócios  
✔ Aplicar boas práticas de escrita e organização de queries SQL  
✔ Visualizar resultados e tendências utilizando Power BI  

---

## ⚙️ Estrutura do Projeto

| Arquivo / Pasta | Descrição |
|-----------------|------------|
| **sql-data-credit.ipynb - Colab.pdf** | Notebook em formato PDF com o passo a passo da análise SQL, consultas executadas e outputs documentados |
| **queries/** | Conjunto de arquivos `.sql` com as principais consultas executadas |
| **graphics/** | Diretório contendo os gráficos exportados e utilizados na análise (Power BI e Matplotlib) |
| **datasets/** | Amostras de dados utilizadas nos testes e resultados intermediários |

---

## 🧩 Stack Utilizada

| Categoria | Ferramentas |
|------------|-------------|
| **Linguagem** | SQL |
| **Ambiente de Execução** | Google Colab, AWS Athena |
| **Armazenamento** | AWS S3 |
| **Visualização** | Power BI |
| **Bibliotecas Python (apoio)** | Pandas, Matplotlib |
| **Documentação** | Markdown e Jupyter Notebook |

---

## 🧱 Estrutura da Base de Dados

A tabela principal criada chama-se **`credito`**, e foi armazenada em um bucket S3.  
A criação foi realizada via **Athena** com a seguinte query base:

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS default.credito ( 
  idade int,
  sexo string,
  dependentes int,
  escolaridade string,
  estado_civil string,
  salario_anual string,
  tipo_cartao string,
  qtd_produtos bigint,
  iteracoes_12m int,
  meses_inativo_12m int,
  limite_credito float,
  valor_transacoes_12m float,
  qtd_transacoes_12m int
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES ('serialization.format' = ',', 'field.delim' = ',')
LOCATION "s3://<bucket-name>/"
TBLPROPERTIES ('has_encrypted_data'='false');

---

## 📊 Principais Consultas SQL
As queries desenvolvidas cobrem desde a exploração básica até análises comparativas e relacionais.
Abaixo alguns exemplos representativos:

🔹 Estrutura e Amostra
sql
Copiar código
SELECT * FROM credito LIMIT 10;
🔹 Quantidade total de registros
sql
Copiar código
SELECT COUNT(*) FROM credito;
🔹 Distribuição por escolaridade
sql
Copiar código
SELECT escolaridade, COUNT(*) 
FROM credito 
GROUP BY escolaridade;
🔹 Distribuição por faixa salarial
sql
Copiar código
SELECT salario_anual, COUNT(*) 
FROM credito 
GROUP BY salario_anual;
🔹 Limite máximo de crédito por escolaridade e tipo de cartão
sql
Copiar código
SELECT MAX(limite_credito) AS limite_credito, escolaridade, tipo_cartao, sexo 
FROM credito 
GROUP BY escolaridade, tipo_cartao, sexo;
🔹 Valor médio e máximo de transações por gênero
sql
Copiar código
SELECT MAX(valor_transacoes_12m) AS maior_valor_gasto, 
       AVG(valor_transacoes_12m) AS media_valor_gasto, 
       MIN(valor_transacoes_12m) AS menor_valor_gasto, 
       sexo
FROM credito 
GROUP BY sexo;

--- 

## 📈 Análises Realizadas
Perfil dos clientes: faixa etária, gênero, escolaridade e estado civil

Distribuição de renda e tipos de cartão

Volume de transações e limite de crédito médio por grupo demográfico

Comparativo entre gêneros e faixas de salário

Correlação entre escolaridade e limite de crédito

Proporção de clientes inativos e volume de compras anuais

Essas análises foram complementadas com gráficos interativos no Power BI, permitindo explorar insights como:

📊 Diferenças de limite de crédito por faixa de renda
📉 Relação entre inatividade e número de produtos adquiridos
📈 Comparativo de comportamento de consumo entre gêneros

---

## 🧠 Habilidades Demonstradas
✅ Criação e manipulação de tabelas SQL em ambiente cloud (AWS Athena)
✅ Escrita de queries analíticas complexas com funções de agregação
✅ Limpeza e tratamento de dados com SQL
✅ Geração de relatórios analíticos e dashboards interativos
✅ Integração entre SQL, Python e Power BI
✅ Documentação técnica e estruturação de projeto reprodutível

---

## 📎 Execução
Este projeto foi desenvolvido e documentado em ambiente Google Colab e armazenado no formato PDF:
sql-data-credit.ipynb - Colab.pdf

Os gráficos complementares foram desenvolvidos em Power BI, utilizando o mesmo dataset público disponível em:
🔗 https://github.com/andre-marcos-perez/ebac-course-utils/tree/main/dataset

---

✍️ Autora: [Marina França]
🎓 Formação em Ciência de Dados – EBAC
📅 Projeto da Trilha de SQL para Análise de Dados