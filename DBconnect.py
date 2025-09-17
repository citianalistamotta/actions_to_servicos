import os
from dotenv import load_dotenv
import pymssql


def retornaConexao():
    # Pega diretamente das variáveis de ambiente (definidas nos Secrets do GitHub Actions)
    server_parts = os.environ["DB_SERVER"].split(',')
    server = server_parts[0]
    port = int(server_parts[1]) if len(server_parts) > 1 else 1433
    database = os.environ["DB_NAME"]
    username = os.environ["DB_USER"]
    password = os.environ["DB_PASS"]

    try:
        conn = pymssql.connect(
            server=server,
            port=port,
            user=username,
            password=password,
            database=database
        )
        print("✅ Conexão com o banco estabelecida com sucesso (pymssql)!")
    except pymssql.Error as ex:
        print(f"❌ Erro ao conectar ao banco de dados: {ex}")
        exit(1)

    # Rodar o histórico
    Historico().get_valorOrdenadoCompleto()

    conn.close()
    EOF