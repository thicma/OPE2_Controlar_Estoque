from models import Tipo_Autorizacao, Tamanho_Produto
import mysql.connector
import formata_instrucao_sql
from daoEstoque import criar_tamanho

dao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'admin',
    database = 'estoque'
)

cursor = dao.cursor()
valores = []

objeto_a_ser_criado = int(input("""
Informe:
1 - para CRIAR Tamanho do Produto
2 - para CRIAR Usuario
3 - para CRIAR Fornecedor
4 - para CRIAR Tipo de Autorização
"""))

if objeto_a_ser_criado == 1:
    id_tamanho = input('Informe PP, P, M, G, GG\n').upper()
    tamanhos = {'PP':'extra pequeno', 'P':'Pequeno', 'M':'Médio', 'G':'Grande', 'GG':'Extra Grande'}
    tamanho_criado = Tamanho_Produto(id_tamanho, tamanhos[id_tamanho].lower())
    tupla = (tamanho_criado.id_tamanho, tamanho_criado.descricao_tamanho,)
    criar_tamanho(tupla)
    

