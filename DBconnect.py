import os
from dotenv import load_dotenv
import pymssql

load_dotenv()

def retornaConexao():
    server = os.getenv("DB_SERVER").split(',')[0]  # remove a porta
    port = int(os.getenv("DB_SERVER").split(',')[1])
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")

    try:
        cnxn = pymssql.connect(
            server=server,
            port=port,
            user=username,
            password=password,
            database=database
        )
        print("Conexão com o banco estabelecida com sucesso (pymssql)!")
        return cnxn
    except pymssql.Error as ex:
        print(f"Erro ao conectar ao banco de dados: {ex}")
        return None
