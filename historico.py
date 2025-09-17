from DBconnect import retornaConexao
import os
import pandas as pd
from datetime import datetime, timedelta


class Historico():
    def __init__(self):
        self.cnxn = retornaConexao()
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def get_valorOrdenadoCompleto(self):
        if not self.cnxn:
            print("Não foi possível executar a query porque a conexão falhou.")
            return None

        data_anterior = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  
        with open('Servicos.sql', 'r', encoding='UTF-8') as file:
            query = file.read()
            query = query.format(dataParam=data_anterior) 

        df = pd.read_sql(query, self.cnxn, index_col=None)
        self.cnxn.close()

        print("Colunas retornadas:", df.columns.tolist())

        # Normaliza nomes das colunas
        df.columns = df.columns.str.strip()

        # Conversões numéricas
        for col in ["R$/KM", "IAP%", "RPK", "ASK"]:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

        df_filtrado = df[df['R$/KM'] > 0.00]

        print('------------------ df_filtrado ------------------')
        print(df_filtrado.head(10))  # só mostra 10 primeiras linhas
        print('-------------------------------------------------')

        # Agrupamento
        df_agrupado = df_filtrado.groupby(['Linha', 'Horário'], as_index=False).agg({
            'R$/KM': 'sum',
            'RPK': 'sum',
            'ASK': 'sum'
        })

        # Cálculo do IAP Real
        df_agrupado['IAP%'] = (df_agrupado['RPK'] / df_agrupado['ASK']).fillna(0)
        df_agrupado['IAP%'] = (df_agrupado['IAP%'] * 100).round(2)

        # Ordena por R$/KM
        df_ordenado = df_agrupado.sort_values(by='R$/KM', ascending=False)

        print('------------------ df_ordenado ------------------')
        print(df_ordenado.head(10))  # só mostra 10 primeiras linhas
        print('-------------------------------------------------')

        return df_ordenado
