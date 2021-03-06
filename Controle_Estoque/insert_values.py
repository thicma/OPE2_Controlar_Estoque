import mysql.connector


dao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'admin',
    database = 'estoque'
)

cursor = dao.cursor()

sql_table_produto = '''INSERT INTO PRODUTO (CODIGO, COR, PRECO, QUANTIDADE, TIPO, TAMANHO, MARCA)
                    VALUES (%s,%s,%s,%s,%s,%s,%s);'''
values_produto = ('cms1', 'branca', 29.90, 20, 1, 'M', 'Lobo Marinho')

sql_table_fornecedor = '''INSERT INTO FORNECEDOR (COD_FORNECEDOR, NOME, EMAIL, TELEFONE, CNPJ)
                    VALUES (%s,%s,%s,%s,%s);'''
values_fornecedor = [(1050, 'A Casa dos Lobos', 'casadoslobos@gmail.com', '1126616662', '11550770002030'),
                    (1080, 'Camisa de Vento', 'camisadevento@gmail.com', '1126617712', '11440880005001')]

sql_table_marca = '''INSERT INTO marca (nome_marca, fornecedor)
                    VALUES (%s,%s);'''
values_marca = ('Lobo Marinho', 1050)

sql_table_tamanho = '''INSERT INTO tamanho (id_tamanho, descricao_tamanho)
                    VALUES (%s,%s);'''
values_tamanho = [('PP','Extra Pequeno'),
                    ('P','Pequeno'),
                    ('M', 'Médio'),
                    ('G', 'Grande'),
                    ('GG', 'Extra Grande')]
sql_table_tipo = '''INSERT INTO tipo (id_tipo, descricao, material, modelo, ano_colecao)
                    VALUES (%s,%s,%s,%s,%s);'''
values_tipo = [(1, 'Camiseta', 'Algodão', 'Gola V', 2020),(2, 'Calça', 'Jeans', 'Cintura Alta', 2021)]

sql_table_tipo_transacao = '''INSERT INTO tipo_transacao (codigo_transacao, nome_transacao, nivel_transacao)
                    VALUES (%s,%s,%s);'''
values_tipo_transacao = [(1, 'Consultar', 1),(2,'Baixar', 2), (3,'Repor', 3), (4, 'Solicitar',2)]

sql_table_transacao = '''INSERT INTO transacao (usuario, cod_produto, tipo_transacao)
                    VALUES (%s,%s,%s);'''
values_transacao = [(506, 'cms1', 1),(106, 'cms1', 4)]

sql_table_usuario = '''INSERT INTO usuario (matricula, senha, nome, cargo, autorizacao) 
                        VALUES (%s,%s,%s,%s,%s);'''
values_usuario = [(506, 'Jk&*902365!', 'Thiago Andrade', 'Gerente', 5),
                (106,'12345678','Jobson Roberto', 'Estoquista', 2)]

#cursor.executemany(sql_table_usuario, values_usuario)
#dao.commit()
print(cursor.rowcount, 'was inserted')
cursor.executemany(sql_table_tipo_transacao, values_tipo_transacao)
dao.commit()
print(cursor.rowcount, 'was inserted')
cursor.executemany(sql_table_fornecedor, values_fornecedor)
dao.commit()
print(cursor.rowcount, 'was inserted')
cursor.executemany(sql_table_tamanho, values_tamanho)
dao.commit()
print(cursor.rowcount, 'was inserted')
cursor.executemany(sql_table_tipo, values_tipo)
dao.commit()
print(cursor.rowcount, 'was inserted')
cursor.execute(sql_table_marca, values_marca)
dao.commit()
print(cursor.rowcount, 'was inserted')
cursor.execute(sql_table_produto, values_produto)
dao.commit()
print(cursor.rowcount, 'was inserted')
cursor.executemany(sql_table_transacao, values_transacao)
dao.commit()
print(cursor.rowcount, 'was inserted')
