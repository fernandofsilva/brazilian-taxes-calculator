""" Abril - Bruno - Relatório Negociações"""

import pandas as pd

archive = r'C:\Users\bsimm\Downloads\InfoCEI_Negociacoes_B.xls'

# usecols=('B:K') and "header=10" will be the same everytime ?
arquivo_cei_negociacoes = pd.read_excel(archive, index_col=0, usecols='B:K', header=10)
arquivo_cei_negociacoes

# exclude columns with all values == NaN
arquivo_cei_negociacoes.dropna(axis='columns', how='all', inplace=True)
arquivo_cei_negociacoes

# exclude rows with all values == NaN
arquivo_cei_negociacoes.dropna(axis='rows', how='all', inplace=True)
arquivo_cei_negociacoes

# converting the index (axis=column) to date
arquivo_cei_negociacoes.index = pd.to_datetime(arquivo_cei_negociacoes.index)
arquivo_cei_negociacoes

arquivo_cei_negociacoes.to_excel('arquivo_cei_negociacoes.xlsx')
