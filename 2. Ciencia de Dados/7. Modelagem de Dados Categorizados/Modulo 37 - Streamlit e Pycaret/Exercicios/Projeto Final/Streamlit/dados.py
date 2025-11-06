import streamlit as st
import pandas as pd

df = pd.read_feather('credit_scoring.ftr')

st.title("💳 Entendimento da Base de Dados – Programa de Crédito")

st.markdown("""
## 🧾 Sobre a Base de Dados

Esta base representa o histórico de clientes de um **programa de crédito de um banco**.  
O objetivo é analisar os fatores que influenciam o risco de inadimplência e construir modelos capazes de prever se um cliente tem maior ou menor probabilidade de não pagar suas dívidas (*default*).

A base é amplamente utilizada em **projetos de Credit Scoring**, uma das principais aplicações de *Machine Learning* em instituições financeiras.

---

## 📂 Estrutura dos Dados

Cada linha representa um **cliente**, e cada coluna traz uma característica relevante para a análise de risco de crédito.
Com a seguinte estrutura de linhas e colunas:""")

st.write(df.shape)

st.markdown("""
| Coluna | Descrição |
|:--|:--|
| `id` | Identificador único do cliente |
| `idade` | Idade do cliente em anos |
| `qtd_filhos` | Quantidade de filhos declarada |
| `tempo_emprego` | Tempo (em anos) de vínculo empregatício atual |
| `salario_anual` | Faixa ou valor anual de salário informado |
| `score_credito` | Pontuação interna do cliente com base no histórico de crédito |
| `qtd_contas` | Quantidade de contas bancárias ou produtos ativos |
| `estado_civil` | Estado civil do cliente (Solteiro, Casado etc.) |
| `genero` | Gênero informado (M/F) |
| `default` | Variável alvo: indica se o cliente apresentou inadimplência (`1`) ou não (`0`) |

---

## 🎯 Objetivo Analítico

A análise desta base busca responder perguntas como:
- Quais características mais influenciam o risco de inadimplência?
- É possível prever o comportamento futuro dos clientes com base nos dados históricos?
- Quais perfis de clientes são mais propensos a pagar em dia?

Essas informações são fundamentais para **definir políticas de crédito mais seguras**, melhorar o processo de aprovação e reduzir perdas financeiras do banco.

---

## 🪙 Base de Dados

Tendo em vista a introdução anterior apresenta-se a seguir a base de dados a ser estudada:""")

st.write(df)
