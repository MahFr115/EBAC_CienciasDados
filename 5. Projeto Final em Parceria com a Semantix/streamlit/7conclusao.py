import streamlit as st



st.title("🎶 Previsão de Demanda para Shows Musicais em São Paulo")

st.header("🎶 Conclusão")

st.write("""Este projeto demonstrou como técnicas de ciência de dados e aprendizado de máquina podem ser aplicadas de forma prática ao mercado 
de eventos musicais em São Paulo. A partir da integração de diferentes fontes de dados — envolvendo artistas, locais, datas, festivais e 
contexto temporal — foi possível construir um modelo capaz de estimar a lotação esperada de shows de médio e grande porte.

Após etapas de limpeza, padronização e análise exploratória, observou-se que fatores estruturais, como a categoria do local, a sazonalidade e a 
realização de festivais, exercem influência mais consistente sobre o público do que métricas isoladas de popularidade dos artistas. Esses 
padrões foram incorporados à modelagem preditiva, resultando em um modelo baseado em árvores de decisão (Extra Trees Regressor) com bom 
desempenho e estabilidade.

O simulador apresentado nesta aplicação permite explorar diferentes cenários de forma interativa, auxiliando na tomada de decisão sobre local, 
período e tipo de evento. As previsões devem ser interpretadas como estimativas de apoio ao planejamento, e não como valores absolutos, 
considerando as limitações inerentes aos dados disponíveis e à natureza dinâmica do mercado de eventos.

Por fim, a aplicação em Streamlit transforma o modelo em uma ferramenta acessível, permitindo que usuários sem conhecimento técnico possam 
utilizar os resultados de maneira intuitiva. O projeto reforça o potencial da ciência de dados como suporte estratégico no setor cultural e 
pode ser expandido futuramente com novas fontes de dados, como vendas antecipadas, marketing digital e preços dinâmicos.""")