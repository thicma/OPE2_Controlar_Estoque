import mysql.connector

dao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'admin',
    database = 'estoque'
)

cursor = dao.cursor()

SQL_INSERT_TAMANHO_PRODUTO = 'Insert Into TAMANHO_PRODUTO (ID_TAMANHO_PRODUTO, DESCRICAO_TAMANHO) VALUES(%s,%s);'

def criar_tamanho(tamanho: tuple):
    valores = tamanho
    cursor.execute(SQL_INSERT_TAMANHO_PRODUTO, valores)
    dao.commit()
    cursor.execute('select * from tamanho_produto;')
    for x in cursor:
        print(x)