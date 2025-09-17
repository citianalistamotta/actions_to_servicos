import pandas as pd
from datetime import datetime, timedelta
from historico import Historico
from contatos import Contatos
import pyperclip
import time as tm
import os



class Relatorio():
    def __init__(self):
        self.historico = Historico()
  
    def relatorioServicos(self):
        df = self.historico.get_valorOrdenadoCompleto()

        # Converte a coluna 'R$/KM' para numérico
        df['R$/KM'] = df['R$/KM'].astype(str).str.replace(',', '.').astype(float).round(2)

        # Filtra os TOP 5 resultados (maiores valores de R$/KM)
        top_5 = df.nlargest(5, 'R$/KM')

        # Filtra os piores resultados (R$/KM menor que 4 e diferente de zero)
        piores_resultados = df[(df['R$/KM'] < 4) & (df['R$/KM'] != 0)]

        # Cria a pasta se não existir
        output_dir = 'reports/reportsoutput'
        os.makedirs(output_dir, exist_ok=True)
        
        with open(f'reports/reportsoutput/relatorioServicos.txt', 'w', encoding='utf-8') as RelatorioServicos:
            msgData = (datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y')
            RelatorioServicos.write("*RELATÓRIO DE SERVIÇOS DIÁRIOS*\n")
            RelatorioServicos.write(f"📅 *DIA:  *{msgData}:*\n\n")
            
            RelatorioServicos.write("----- *TOP 5 RESULTADOS* -----\n\n")
            for _, row in top_5.iterrows():
                RelatorioServicos.write(
                    f"""🏆{row['Linha']}\n🕝{row['Horário']}\n💲R$/KM: {row['R$/KM']}\n💺IAP%: {row['IAP%']}\n\n"""
                )

            RelatorioServicos.write("----- *PIORES RESULTADOS* -----\n")
            totalPiores = len(piores_resultados)  # Obtém a quantidade de linhas em piores_resultados
            RelatorioServicos.write(f"📊TOTAL: {totalPiores}\n\n")
            for _, row in piores_resultados.iterrows():
                RelatorioServicos.write(
                    f"""⚠️{row['Linha']}\n🕝{row['Horário']}\n💲R$/KM: {row['R$/KM']}\n💺IAP%: {row['IAP%']}\n\n"""
                )

  