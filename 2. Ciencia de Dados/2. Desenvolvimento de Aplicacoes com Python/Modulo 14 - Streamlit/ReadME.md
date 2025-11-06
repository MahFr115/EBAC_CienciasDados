# 🌐 Módulo 14 – Streamlit I: Introdução e Fundamentos

Este módulo marca o início do desenvolvimento de **aplicações web interativas para Ciência de Dados** utilizando o Streamlit — uma ferramenta que permite transformar scripts Python em interfaces visuais de forma rápida e intuitiva, sem a necessidade de conhecimentos avançados em front-end.

---

## 🎯 Objetivos do Módulo

✔ Instalar e configurar o Streamlit  
✔ Executar a primeira aplicação interativa  
✔ Criar elementos básicos de interface (texto, cabeçalhos, sliders)  
✔ Utilizar comandos para exibição de conteúdo e gráficos  
✔ Aprender a estruturar páginas com Markdown e HTML  
✔ Preparar fundamentos para construção de dashboards interativos  

---

## ⚙️ Fluxo inicial de uso do Streamlit

| Etapa | Ação | Comando |
|-------|------|---------|
| Instalação | Instalação via terminal | `pip install streamlit` |
| Execução inicial | Exemplo interativo padrão | `streamlit hello` |
| Execução de script próprio | Uso de um arquivo Python | `streamlit run nome_do_script.py` |

---

## 📌 Comandos e componentes introduzidos

| Comando / Conceito | Descrição |
|-------------------|-----------|
| `write()` | Exibe conteúdo textual, similar ao `print()`, mas adaptado para interface web |
| `markdown()` | Permite criar texto formatado usando sintaxe Markdown |
| `header()` / `subheader()` | Criam títulos hierárquicos para organizar a página |
| HTML em Markdown | Uso de tags HTML para customização visual (com `unsafe_allow_html=True`) |
| `slider` | Componente interativo para selecionar valores |
| `st.pyplot()` | Exibe gráficos criados com Matplotlib na aplicação |

---

## 📑 Glossário do Módulo

Os principais termos técnicos utilizados nesta etapa estão documentados no arquivo **`Glossario.pdf`**, incluindo:  
🔹 `Instalar o Streamlit` • `streamlit hello` • `Comando run`  
🔹 `write()` • `header` • `subheader`  
🔹 `HTML em Markdown` • `Slider` • `st.pyplot()`  

📎 *Local do arquivo: `./Glossario.pdf`* :contentReference[oaicite:0]{index=0}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Propósito |
|-----------|-----------|
| **Streamlit** | Criação de aplicações web interativas |
| **Python** | Base de desenvolvimento |
| **Matplotlib** | Visualização de gráficos exibidos na interface |
| **Markdown / HTML** | Estruturação de conteúdo textual |

---

## 📌 Importância do Módulo

A partir deste módulo, os projetos evoluem de scripts executados em terminal para **interfaces interativas acessíveis e amigáveis**, essenciais para apresentar resultados a stakeholders, criar dashboards e prototipar soluções de forma ágil.