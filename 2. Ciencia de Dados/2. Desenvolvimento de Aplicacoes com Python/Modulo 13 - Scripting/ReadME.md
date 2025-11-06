# ⚙️ Módulo 13 – Scripting aplicado à Ciência de Dados

Este módulo introduz a criação de **scripts automatizados em Python** para gerar análises recorrentes, permitindo substituir execuções manuais por rotinas reproduzíveis e agendáveis. O foco é transformar fluxos interativos de análise (como em notebooks) em **processos automatizados e replicáveis**, prontos para uso recorrente ou integração em pipelines de dados.

---

## 🎯 Objetivos do Módulo

✔ Entender o conceito e a finalidade de um script  
✔ Criar uma rotina automatizada para geração de relatórios mensais  
✔ Trabalhar com **arquivos e diretórios via pacote OS**  
✔ Aprender a salvar visualizações automaticamente com `savefig()`  
✔ Utilizar argumentos via linha de comando usando `sys.argv`  
✔ Tornar o código **replicável e reutilizável**  
✔ Publicar um script em uma aplicação com **Streamlit** (introdução)

---

## 📂 Conteúdo Abordado

| Tema | Descrição |
|------|-----------|
| O que é Scripting | Sequência automatizada de comandos para execução sem intervenção |
| Script replicável | Código que pode ser usado novamente com ajustes mínimos |
| Geração de relatórios mensais | Automação de rotinas analíticas recorrentes |
| Pacote OS | Criação e gerenciamento de diretórios |
| `exist_ok=True` | Evita erros ao criar pastas já existentes |
| Salvamento de gráficos | Uso da função `savefig()` |
| Argumentos de linha de comando | Tornam scripts mais flexíveis e dinâmicos |
| `sys.argv` | Captura de argumentos fornecidos na execução do script |
| Código ao vivo vs script | Diferença entre execução interativa e automatizada |
| Streamlit | Uso introdutório para criar dashboards a partir de scripts |

---

## 📑 Glossário do Módulo

Os seguintes conceitos são abordados detalhadamente no arquivo **`Glossario.pdf`**:

✅ Script • Código replicável • Código ao vivo  
✅ Pacote OS • `os.makedirs()` • `exist_ok=True`  
✅ Savefig • Argumentos de linha de comando • `sys.argv`  
✅ Streamlit • Base SINASC • Análises mensais  

📎 *Local do arquivo: `./Glossario.pdf`* :contentReference[oaicite:1]{index=1}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Finalidade |
|-----------|-----------|
| **Python 3.x** | Linguagem usada na construção dos scripts |
| **Pacote OS** | Manipulação de diretórios |
| **Matplotlib** | Criação e salvamento de visualizações com `savefig()` |
| **Pandas** | Tratamento de dados dentro do script |
| **sys** | Captura de argumentos de execução (`sys.argv`) |
| **Streamlit** | Interface interativa baseada no script (introdução) |
| **Editor de texto / VS Code / IDE** | Criação e edição do script |

---

## 📌 Importância do Módulo

Dominar scripting é uma habilidade essencial para cientistas de dados que desejam:

✅ Automatizar cargas, análises e relatórios periódicos  
✅ Reutilizar rotinas analíticas com diferentes parâmetros  
✅ Criar pipelines automatizados e integrá-los com ETL e MLOps  
✅ Transformar análises interativas em soluções prontas para stakeholders  
✅ Evoluir notebooks para aplicações executáveis ou dashboards  