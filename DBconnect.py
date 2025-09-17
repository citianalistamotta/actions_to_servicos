import pyodbc

def retornaConexao():
    server = 'smarttravel-rds-mssql-n7ws.c9aakyyow4vn.us-east-2.rds.amazonaws.com,1433'  
    database = 'BI_Motta_PROD' 
    username = 'motta_bi_smartbus'  
    password = 'Abc`"@+t|,,D/gj='  
    driver = '{ODBC Driver 17 for SQL Server}'  

    try:
        cnxn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        return cnxn
    except pyodbc.Error as ex:
        print(f"Erro ao conectar ao banco de dados: {ex}")
        return None
    except Exception as e:
        print(f"Erro desconhecido ao conectar ao banco de dados: {e}")
        return None
