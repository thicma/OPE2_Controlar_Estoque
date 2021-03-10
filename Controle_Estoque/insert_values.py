import mysql.connector
import formata_instrucao_sql


dao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'admin',
    database = 'estoque'
)

cursor = dao.cursor()
valores = []

def cria_lista_de_tabelas():
    tabelas_existentes = []
    cursor.execute('show tables;')
    for posicao, tabela in enumerate (cursor):
        tabelas_existentes.append(tabela[0])    
    return tabelas_existentes

def valida_escolha_da_tabela(nome_informado_pelo_usuario, tabelas_existentes):
    if nome_informado_pelo_usuario in tabelas_existentes:
        return cria_lista_com_nome_das_colunas(nome_informado_pelo_usuario)
    return ('Nome de tabela inválido. ')

def cria_lista_com_nome_das_colunas(tabela):
    nome_colunas = []
    cursor.execute(f'SHOW COLUMNS FROM {tabela}')
    for posicao, nome in enumerate (cursor):    
        nome_colunas.append(nome[0])
    return nome_colunas


tabelas_existentes = cria_lista_de_tabelas()
nome_tabela = input('Informe o nome da tabela: ')
colunas_tabelas = valida_escolha_da_tabela(nome_tabela, tabelas_existentes)


'''
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
'''