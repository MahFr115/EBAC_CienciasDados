import numpy as np
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt


def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).unstack().plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return None

def nome_arquivos():
    meses_dict = {
        'JANEIRO': 'JAN', 'FEVEREIRO': 'FEV', 'MARÇO': 'MAR', 'ABRIL': 'ABR',
        'MAIO': 'MAI', 'JUNHO': 'JUN', 'JULHO': 'JUL', 'AGOSTO': 'AGO',
        'SETEMBRO': 'SET', 'OUTUBRO': 'OUT', 'NOVEMBRO': 'NOV', 'DEZEMBRO': 'DEZ'
    }

    arquivos = []  
    print("Para encerrar o recebimento de valores responda 0 para qualquer pergunta!")

    while True:
        estado = input("Sigla do estado da análise: ").upper()
        
        if estado == "0":
            print("Encerrando entrada de dados...")
            break  # Para o loop se estado for "0"
        
        mês = input("Nome do mês do relatório: ").upper()
        
        if mês == "0":
            print("Encerrando entrada de dados...")
            break  # Para o loop se mês for "0"
        
        if mês not in meses_dict:
            print("Mês inválido! Tente novamente.")
            continue  

        ano = input("Ano do relatório (AAAA): ")
        
        if ano == "0":
            print("Encerrando entrada de dados...")
            break  # Para o loop se ano for "0"

        arquivo = f'./input/SINASC_{estado}_{ano}_{meses_dict[mês]}.csv'
        arquivos.append(arquivo)
        print(f"Arquivo adicionado: {arquivo}")

    return arquivos  

# Função principal para processar os arquivos e gerar os gráficos
def gerar_relatorios():
    arquivos = nome_arquivos()

    for arquivo in arquivos:
        try:
            sinasc = pd.read_csv(arquivo)
            print(f"Processando {arquivo}...")
            print(sinasc.DTNASC.min(), sinasc.DTNASC.max())

            max_data = sinasc.DTNASC.max()[:7]
            print(max_data)
            os.makedirs(f'./output/figs/{max_data}', exist_ok=True)

            # Geração de gráficos
            plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'count', 'quantidade de nascimento', 'data de nascimento')
            plt.savefig(f'./output/figs/{max_data}/quantidade de nascimento.png')
            plt.close()  # Fecha o gráfico para liberar memória

            plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae', 'data de nascimento', 'unstack')
            plt.savefig(f'./output/figs/{max_data}/media idade mae por sexo.png')
            plt.close()

            plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe', 'data de nascimento', 'unstack')
            plt.savefig(f'./output/figs/{max_data}/media peso bebe por sexo.png')
            plt.close()

            plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'apgar1 medio', 'gestacao', 'sort')
            plt.savefig(f'./output/figs/{max_data}/media apgar1 por escolaridade mae.png')
            plt.close()

            plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio', 'gestacao', 'sort')
            plt.savefig(f'./output/figs/{max_data}/media apgar1 por gestacao.png')
            plt.close()

            plota_pivot_table(sinasc, 'APGAR5', 'GESTACAO', 'mean', 'apgar5 medio', 'gestacao', 'sort')
            plt.savefig(f'./output/figs/{max_data}/media apgar5 por gestacao.png')
            plt.close()

            print(f"Relatórios gerados para {arquivo} em ./output/figs/{max_data}")

        except FileNotFoundError:
            print(f"Arquivo não encontrado: {arquivo}")
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")

# Executa o script
if __name__ == "__main__":
    gerar_relatorios()