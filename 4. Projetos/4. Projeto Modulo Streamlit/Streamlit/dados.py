import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport

st.title("Ciências de Dados - EBAC")
st.header("Análise Descritiva")

st.write("Neste exercício vamos usar a base online shoppers purchase intention de Sakar, C.O., Polat, S.O., Katircioglu, M. et al. " \
"Neural Comput & Applic (2018). [Web Link](https://link.springer.com/article/10.1007/s00521-018-3523-0).")

############################################################################################################
### Ler os arquivos
df = pd.read_csv("online_shoppers_intention.csv")
st.write("Pré-visualização dos dados:")
st.dataframe(df)
##########################################################################################################
# Variáveis
st.write("A seguir descreve-se as variáveis da base de dados")

html_table = '''<table>
  <tr>
    <th>Variável</th>
    <th>Descrição</th>
  </tr>
  <tr><td>Administrative</td><td>Quantidade de acesso em páginas administrativas</td></tr>
  <tr><td>Administrative_Duration</td><td>Tempo de acesso em páginas administrativas</td></tr>
  <tr><td>Informational</td><td>Quantidade de acesso em páginas informativas</td></tr>
  <tr><td>Informational_Duration</td><td>Tempo de acesso em páginas informativas</td></tr>
  <tr><td>ProductRelated</td><td>Quantidade de acesso em páginas de produtos</td></tr>
  <tr><td>ProductRelated_Duration</td><td>Tempo de acesso em páginas de produtos</td></tr>
  <tr><td>BounceRates</td><td>*Percentual de visitantes que entram no site e saem sem acionar outros requests durante a sessão</td></tr>
  <tr><td>ExitRates</td><td>* Soma de vezes que a página é visualizada por último em uma sessão dividido pelo total de visualizações</td></tr>
  <tr><td>PageValues</td><td>* Representa o valor médio de uma página da Web que um usuário visitou antes de concluir uma transação de comércio eletrônico</td></tr>
  <tr><td>SpecialDay</td><td>Indica a proximidade a uma data festiva (dia das mães etc)</td></tr>
  <tr><td>Month</td><td>Mês</td></tr>
  <tr><td>OperatingSystems</td><td>Sistema operacional do visitante</td></tr>
  <tr><td>Browser</td><td>Browser do visitante</td></tr>
  <tr><td>Region</td><td>Região</td></tr>
  <tr><td>TrafficType</td><td>Tipo de tráfego</td></tr>
  <tr><td>VisitorType</td><td>Tipo de visitante: novo ou recorrente</td></tr>
  <tr><td>Weekend</td><td>Indica final de semana</td></tr>
  <tr><td>Revenue</td><td>Indica se houve compra ou não</td></tr>
</table>'''

st.write(html_table, unsafe_allow_html=True)

st.write("--------------------------------------------------------------------------------------------------")
#####################################################################################################
st.subheader("Estrutura dos dados")

prof = ProfileReport(df, explorative=True, minimal=True)
report_html = prof.to_html()
st.write("Profiling Report")
st.components.v1.html(report_html, width=50000, height=1000, scrolling=True)

st.write("--------------------------------------------------------------------------------------------------")

st.write("Não há missing values entre os dados estudados. Entretanto, há uma grande quantidade de dados numéricos iguais a 0, variando entre, " \
"aproximadamente 9\% dos dados da variável ProductRelated_Duration à, aproximadamente, 90\% dos dados de SpecialDay. A distribuição dos dados " \
"observados segue uma padronização entre os valores não nulos, estando distribuidos de forma semelhantes e/ou havendo uma distribuição muito " \
"semelhante a uma regressão linear.")
st.write("Percebemos uma grande variabilidade dos valores de tempo de duração de visitas no site, considerando a descrição das variáveis " \
"entende-se que essa diferença entre valores é comum e não é nescessário uma padronização deles.")
st.write("Entretanto o valor de tipo de visitantes (novos visitantes, visitantes recorrentes ou outros ) tem poucas repostas como \"others\" "
"(85), então, podemos considerar esse valor como irrelevante, e os exluirei, uma vez que essa resposta não parece ter significado de " \
"importância. Assim reduzirei as possibilidades de respostas para essa pergunta.")
