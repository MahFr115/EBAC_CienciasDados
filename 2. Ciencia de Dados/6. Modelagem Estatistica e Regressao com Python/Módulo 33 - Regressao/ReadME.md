# 📉 Módulo 33 – Regressão III

Neste módulo, a jornada em regressão é aprofundada com foco na **inferência dentro dos modelos**, interpretação de variáveis, ajustes para dados **não lineares** e novos métodos de ajuste como **regressão segmentada e LOWESS**.

A compreensão de como interpretar e transformar os dados dentro de um modelo de regressão é essencial para construir previsões mais robustas e coerentes com o comportamento real dos dados.

---

## 🎯 Objetivos do Módulo

✔ Fazer inferência estatística dentro de modelos de regressão  
✔ Interpretar o intercepto e parâmetros estimados  
✔ Construir intervalos de confiança para previsões  
✔ Tratar relações não lineares por meio de transformações  
✔ Aplicar regressão segmentada para diferentes comportamentos no mesmo modelo  
✔ Identificar pontos de mudança (Constante C0)  
✔ Utilizar LOWESS/LOESS como técnica de suavização  
✔ Automatizar cortes com `pd.qcut` para categorizar variáveis  

---

## 📚 Conteúdo Abordado (com base no glossário)

| Tema | Descrição |
|------|-----------|
| Intercepto | Valor de Y quando todas as variáveis explicativas são zero |
| Intervalo de confiança | Intervalo provável de conter um parâmetro verdadeiro |
| Relações não lineares | Comportamentos que não são representados por uma reta |
| Transformação Logarítmica | Uso de log para ajustar não linearidade |
| Regressão Segmentada | Modelo com mudança na inclinação a partir de C0 |
| Constante C0 | Ponto em que a reta muda de inclinação |
| LOWESS/LOESS | Suavização ponderada para ajuste local |
| Função de interpolação | Estima valores entre pontos conhecidos |
| `pd.qcut` | Divide variáveis contínuas em categorias com quantis |

📎 Glossário completo disponível em: **Profissão Cientista de Dados M34 Glossário.pdf** :contentReference[oaicite:1]{index=1}

---

## 🛠 Ferramentas Utilizadas

| Ferramenta | Aplicação |
|-----------|-----------|
| `statsmodels` | Ajuste da regressão e criação de intervalos |
| `sklearn` | Suporte na modelagem com transformações |
| `pd.qcut` | Categorização baseada em quantis |
| `numpy.log()` | Aplicação de transformação logarítmica |
| `lowess` (do `statsmodels`) | Aplicação de suavização |
| `matplotlib` / `seaborn` | Visualização de curvas segmentadas e suavizadas |

---

## 📌 Importância do Módulo

A regressão raramente é estritamente linear na prática. Este módulo prepara o aluno para:

✅ Ajustar modelos a comportamentos reais dos dados  
✅ Interpretar resultados com suporte estatístico  
✅ Melhorar previsões por meio de transformações adequadas  
✅ Detectar mudanças de regime em relações entre variáveis  
✅ Tratar não linearidade sem migrar imediatamente para modelos mais complexos  