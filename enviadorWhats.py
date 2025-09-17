import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from contatos import Contatos  # Contatos definidos no contatos.py

load_dotenv()  # Carrega as variáveis do .env

class EnviadorWhats:
    """
    Classe única para envio do relatório de serviços via Z-API.
    Lê token e id da instância do .env e contatos do contatos.py
    """

    def __init__(self):
        self.token = os.getenv("ZAPI_TOKEN")
        self.id_instancia = os.getenv("ZAPI_INSTANCIA")
        self.contatos = Contatos
        self.url_base = f'https://api.z-api.io/instances/{self.id_instancia}/token/{self.token}'
        self.headers = {"Content-Type": "application/json",
            "Client-Token": os.getenv("ZAPI_CLIENT_TOKEN")}
        # Caminho fixo do relatório
        self.caminho_relatorio = os.path.join("reports", "reportsoutput", "relatorioServicos.txt")

    def enviar_texto(self, telefone: str, mensagem: str):
        """Envia mensagem de texto via Z-API"""
        url = f'{self.url_base}/send-text'
        payload = {"phone": telefone, "message": mensagem}

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response_json = response.json()
        except Exception as e:
            print(f"Erro na requisição para {telefone}: {e}")
            return False

        if response.status_code == 200 and not response_json.get('error'):
            print(f"Mensagem enviada com sucesso para {telefone}")
            return True
        else:
            print(f"Falha ao enviar mensagem para {telefone}: {response.status_code} - {response_json}")
            return False

    def enviar_relatorio(self):
        """Lê o arquivo relatorioServicos.txt e envia para todos os contatos"""
        if not os.path.exists(self.caminho_relatorio):
            print(f"Arquivo não encontrado: {self.caminho_relatorio}")
            return

        with open(self.caminho_relatorio, 'r', encoding="utf-8") as f:
            mensagem = f.read()

        if not mensagem.strip():
            print("Arquivo de relatório vazio.")
            return

        data_hoje = datetime.now().strftime("%Y-%m-%d")

        for nome, numero in self.contatos.items():
            print(f"Enviando relatório para {nome} ({numero})...")
            self.enviar_texto(numero, mensagem)
