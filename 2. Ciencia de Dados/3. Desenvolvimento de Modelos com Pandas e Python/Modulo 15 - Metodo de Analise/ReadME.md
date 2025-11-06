# 📍 Módulo 15 – Métodos de Análise

Este módulo aprofunda técnicas práticas para tornar análises de dados mais eficientes, legíveis e escaláveis utilizando o **Pandas**, com foco em **encadeamento de métodos, otimização de performance e exploração automatizada**. Aprende-se também a manipular dados de forma avançada por meio de **funções de janela móvel e geração de relatórios rápidos de diagnóstico exploratório**.

---

## 🎯 Objetivos do Módulo

✔ Melhorar a eficiência no processamento de dados usando **method chaining**  
✔ Eliminar variáveis intermediárias desnecessárias para produzir código limpo  
✔ Aplicar o método `.apply()` para personalizar transformações em linhas ou colunas  
✔ Medir performance com `%timeit`  
✔ Explorar automaticamente datasets usando **Pandas Profiling**  
✔ Exportar rapidamente dados com `.to_clipboard()` e `.to_excel()`  
✔ Trabalhar com **funções de janela móvel** (média móvel, soma móvel) para séries temporais  
✔ Entender práticas de análise rápida e escalável em ciência de dados

---

## 📂 Conteúdo Abordado

| Tema | Descrição |
|------|-----------|
| **Method Chaining** | Encadeamento de métodos para criar pipelines limpos |
| **Variáveis Intermediárias** | Uso e impacto na legibilidade do código |
| **assign()** | Criação de novas colunas de forma fluida |
| **apply()** | Aplicação de funções em colunas/linhas (via `axis`) |
| **axis** | Define se a função atua por linha (`axis=1`) ou coluna (`axis=0`) |
| **%timeit** | Medição rápida da performance de trechos de código |
| **Pandas Profiling** | Geração automática de relatórios exploratórios |
| **Colunas constantes** | Detecção de colunas sem valor analítico |
| **Correlação forte** | Relações entre variáveis redundantes |
| **to_clipboard()** | Exportação rápida para Excel via área de transferência |
| **to_excel()** | Salvamento direto em arquivo Excel |
| **Funções de janela móvel** | Análises como média móvel, soma móvel, `shift` |
| **Up & Down Sampling** | Alteração da granularidade temporal ou de amostras |

---

## 📑 Glossário do Módulo

O arquivo **`Glossario.pdf`** contém os principais termos apresentados neste módulo, como:  
➡ *Method Chaining, Variáveis Intermediárias, assign, apply, axis, %timeit, Pandas Profiling, Colunas constantes, Correlações fortes, .to_clipboard(), .to_excel(), Agregação móvel, Média móvel, Soma móvel, Funções up/down, shift.*  
📎 *Local do arquivo: `./Glossario.pdf`* :contentReference[oaicite:1]{index=1}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|-----------|
| **Pandas** | Transformações, agregações e janelas móveis |
| **NumPy** | Suporte computacional para cálculos |
| **Pandas Profiling** | Relatórios automatizados de EDA |
| **Jupyter Notebook** | Execução interativa e testes de performance |
| **Excel / Área de transferência** | Exportação e compartilhamento rápido |

---

## 📌 Importância do Módulo

Este módulo prepara o cientista de dados para análises mais rápidas, expressivas e organizadas, com foco em:

✅ Automação de manipulação de dados  
✅ Melhor legibilidade do código  
✅ Ganhos de performance  
✅ Exploração rápida de datasets  
✅ Base para pipelines de análise e ETL  