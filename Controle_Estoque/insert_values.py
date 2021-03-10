import mysql.connector
import formata_instrucao_sql

tabelas = ['FORNECEDOR','TAMANHO','TIPO','TIPO_TRANSACAO','USUARIO'] 
dao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'Estoque2'
)

cursor = dao.cursor()
valores = []
nome_colunas = []
nome_tabela=''
while (nome_tabela == ''):
	nome_tabela = input('Informe o nome da tabela: ')
	if (nome_tabela not in tabelas):
		print("tabela invalida!")
		nome_tabela=''

cursor.execute(f'show columns from {nome_tabela};')

for posicao, nome in enumerate (cursor):    
    nome_colunas.append(nome[0])

for nome_coluna_atual in nome_colunas:
    valor_informado = input(f'Informe o {nome_coluna_atual}: ')
    valores.append(valor_informado)

nome_colunas = tuple(nome_colunas)
valores = tuple(valores)

cursor.execute(formata_instrucao_sql.formatar_instrucao_sql(nome_tabela, nome_colunas), valores)
for x in range(1,10):
    print('>',end='')
dao.commit()
cursor.execute(f'Select * from {nome_tabela}')

for x in cursor:
    print(x)







    
    

