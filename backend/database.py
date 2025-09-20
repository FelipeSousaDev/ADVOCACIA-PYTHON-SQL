import pyodbc

#Definição das variavéis para o banco de dados
SERVER_NAME = 'FELIPE-PC\\SQLEXPRESS'
DATABASE_NAME = 'ADVOCACIA'

CONNECTION_STRING = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={SERVER_NAME};'
    f'DATABASE={DATABASE_NAME};'
    'Trusted_Connection=yes;'
)
#Testa a conexão com o banco de dados
def get_db_connection():
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        print ("INFO: Conexão com o banco de dados 'ADVOCACIA' bem-sucedida!")
        return conn
    except pyodbc.Error as ex:
        print('Falha com o banco de dados. Verifique as conexões')
        return None