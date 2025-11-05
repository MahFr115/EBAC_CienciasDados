import os
import time
import json
import csv
from random import random
from datetime import datetime
from sys import argv
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # Adicionei a importação do matplotlib.pyplot

URL = 'https://www2.cetip.com.br/ConsultarTaxaDi/ConsultarTaxaDICetip.aspx'

# Criando a variável data e hora 
for _ in range(0, 10):
    data_e_hora = datetime.now()
    data = datetime.strftime(data_e_hora, '%Y/%m/%d')
    hora = datetime.strftime(data_e_hora, '%H:%M:%S')

    # Captando a taxa CDI do site da B3
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.HTTPError as exc:
        print("Dado não encontrado, continuando.")
        cdi = None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        dado = json.loads(response.text)
        cdi = float(dado['taxa'].replace(',', '.')) + (random() - 0.5)

    # Verificando se o arquivo "taxa-cdi.csv" existe
    if not os.path.exists('./taxa-cdi.csv'):
        with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')

    # Salvando dados no arquivo "taxa-cdi.csv"
    with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{cdi}\n')

    time.sleep(2 + (random() - 0.5))

print("Sucesso")

# Lendo os dados do CSV para criar o gráfico
df = pd.read_csv('./taxa-cdi.csv')

# Criando o gráfico usando seaborn
grafico = sns.lineplot(x='hora', y='taxa', data=df)
plt.xticks(rotation=90)  # Ajustar a rotação dos rótulos no eixo x
plt.savefig(f"{argv[1]}.png")
plt.show()
print("Sucesso")