import pandas as pd
from datetime import datetime, timedelta
from historico import Historico
from contatos import Contatos
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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

    def enviarRelatorioServicos(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--profile-directory=Default')
        # options.add_argument(f"--user-data-dir={os.getenv('LOCALAPPDATA')}\\Google\\chrome\\User Data\\")
        options.add_argument(f"--user-data-dir={os.getenv('LOCALAPPDATA')}\\Google\\chrome\\User Data\\BotProfile")
        try:
            navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        except Exception as e:
            print(f"Erro ao iniciar o ChromeDriver: {e}")

        
        with open('reports/reportsoutput/relatorioServicos.txt', 'r', encoding="utf-8") as RelatorioServicos:
            mensagem = RelatorioServicos.read()

            for i in Contatos.values():
                pagina_carregada = False

                while not pagina_carregada:
                    tm.sleep(1)
                    navegador.get(f"https://web.whatsapp.com/send/?phone={i}")
                    navegador.execute_script("window.onbeforeunload = null;")
                    
                    try:
                        elemento = WebDriverWait(navegador, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')))
                        pagina_carregada = True

                    except:
                        print("A página não carregou corretamente. Atualizando...")
                        navegador.get(f"https://web.whatsapp.com/send/?phone={i}")
                        navegador.execute_script("window.onbeforeunload = null;")

                elemento.click()
                pyperclip.copy(mensagem)
                elemento.send_keys(Keys.CONTROL, 'v')
                elemento.send_keys(Keys.ENTER)
                tm.sleep(5)

