import os
import pymssql

def retornaConexao():
    # Lê credenciais do ambiente (preenchidas a partir dos secrets no GitHub Actions)
    server = os.environ.get("DB_SERVER")
    port = int(os.environ.get("DB_PORT", 1433))  # usa 1433 como padrão se não vier nada
    database = os.environ.get("DB_NAME")
    username = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASS")

    try:
        conn = pymssql.connect(
            server=server,
            port=port,
            user=username,
            password=password,
            database=database
        )
        print("✅ Conexão com o banco estabelecida com sucesso (pymssql)!")
        return conn
    except pymssql.Error as ex:
        print(f"❌ Erro ao conectar ao banco de dados: {ex}")
        return None
