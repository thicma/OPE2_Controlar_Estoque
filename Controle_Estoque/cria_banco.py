import mysql.connector

dao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'admin',
)

cursor = dao.cursor()
cria_data_base = '''CREATE DATABASE IF NOT EXISTS Estoque;'''
cursor.execute(cria_data_base)


