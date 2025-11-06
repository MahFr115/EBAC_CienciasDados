import streamlit as st

st.title("🏗️ Projeto: Pipelines e PyCaret no Machine Learning")

st.markdown("""
## 📘 Introdução

Nesta atividade do módulo de *Streamlit e PyCaret*, exploramos a construção de **pipelines de Machine Learning** e o uso do **PyCaret** como ferramenta de automação e comparação de modelos.

O objetivo é compreender como essas abordagens facilitam o fluxo de trabalho de ciência de dados — desde o pré-processamento até a criação de previsões.

---

### 🔄 O que é um *Pipeline*?
Um **pipeline** é uma sequência organizada de etapas de processamento de dados e modelagem.  
Ele permite que todas as transformações (como limpeza, codificação, padronização e treinamento) sejam encadeadas em um único fluxo.  

Isso traz diversas vantagens:
- 🧩 **Organização:** todas as etapas ficam integradas em um mesmo objeto.
- ⚙️ **Reprodutibilidade:** o mesmo processo pode ser aplicado a novos dados facilmente.
- 🚀 **Automação:** facilita a implementação em produção, reduzindo erros manuais.

---

### 🤖 O que é o *PyCaret*?
O **PyCaret** é uma biblioteca de *Machine Learning automatizado (AutoML)* desenvolvida para simplificar o treinamento e a comparação de modelos.  
Com poucas linhas de código, é possível:
- Preparar os dados automaticamente (tratando variáveis categóricas e nulas);
- Treinar dezenas de modelos de forma padronizada;
- Avaliar e comparar os resultados com métricas consistentes;
- Salvar o melhor modelo para uso posterior.

---

### 💡 Por que usar ambos?
- O **pipeline** garante um fluxo de trabalho limpo e reutilizável.  
- O **PyCaret** acelera a experimentação e reduz o tempo de configuração manual.

Juntos, eles tornam o processo de modelagem **mais ágil, confiável e profissional**, unindo automação com boas práticas de engenharia de dados.
""")
