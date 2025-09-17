from utils.DBconnect import retornaConexao
import os
import pandas as pd
from datetime import datetime, timedelta


class Historico():
    def __init__(self):
        self.cnxn = retornaConexao()
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))


    def get_valorOrdenadoCompleto(self):
        data_anterior = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  
        with open('utils/Servicos.sql', 'r', encoding='UTF-8') as file:
            query = file.read()
            query = query.format(dataParam=data_anterior) 

        df = pd.read_sql(query, self.cnxn, index_col=None)

        print("Colunas do df:", df.columns.tolist())

        df.columns = df.columns.str.strip()

        df['R$/KM'] = df['R$/KM'].astype(str).str.replace(',', '.').astype(float)
        df['IAP%'] = df['IAP%'].astype(str).str.replace(',', '.').astype(float)
        df['RPK'] = df['RPK'].astype(str).str.replace(',', '.').astype(float)
        df['ASK'] = df['ASK'].astype(str).str.replace(',', '.').astype(float)

        df_filtrado = df[df['R$/KM'] > 0.00]

        print('------------------ df_filtrado ------------------')
        print(df_filtrado)
        print('-------------------------------------------------')

        # Primeiro, agrupamento das somas
        df_agrupado = df_filtrado.groupby(['Linha', 'Horário'], as_index=False).agg({
            'R$/KM': 'sum',
            'RPK': 'sum',
            'ASK': 'sum'
        })

        # Depois, cálculo do IAP Real
        df_agrupado['IAP%'] = (df_agrupado['RPK'] / df_agrupado['ASK'])
        df_agrupado['IAP%'] = df_agrupado['IAP%'].fillna(0)
        df_agrupado['IAP%'] = (df_agrupado['IAP%'] * 100).round(2)

        # Ordenar por R$/KM
        df_ordenado = df_agrupado.sort_values(by='R$/KM', ascending=False)

        print('------------------ df_ordenado ------------------')
        print(df_ordenado)
        print('-------------------------------------------------')

        return df_ordenado
