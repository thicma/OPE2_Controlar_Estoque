class Usuario:
    def __init__(self, matricula, senha, nome, autorizacao):
        self.matriucla = matricula
        self.senha = senha
        self.nome = nome
        self.autorizacao = autorizacao
    

class Fornecedor:
    def __init__(self, id_fornecedor, nome, email, telefone, cnpj):
        self.id_fornecedor = id_fornecedor
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.cnpj = cnpj

class Tipo_Autorizacao:
    def __init__(self, id_autorizacao, descricao_autorizacao, pode_alterar_produto,
                pode_cadastrar_produto, pode_excluir_produto, pode_consultar_produto,
                pode_solicitar_resposicao_produto):
        
        self.id_autorizacao = id_autorizacao 
        self.descricao_autorizacao = descricao_autorizacao
        self.pode_alterar_produto = pode_alterar_produto
        self.pode_cadastrar_produto =pode_cadastrar_produto
        self.pode_excluir_produto = pode_excluir_produto
        self.pode_consultar_produto = pode_consultar_produto
        self.pode_solicitar_resposicao_produto =  pode_solicitar_resposicao_produto

class Tamanho_Produto:
    def __init__(self, id_tamanho, descricao_tamanho):
        self. id_tamanho = id_tamanho
        self.descricao_tamanho = descricao_tamanho
    
class Tipo_Material:
    def __init__(self, id_material, descricao_material):
        self.id_material = id_material
        self.descricao_material = descricao_material


class Tipo_Produto:
    def __init__(self, id_tipo_produto, descricao_produto, modelo):
        self.id_tipo_produto = id_tipo_produto
        self.descricao_produto = descricao_produto
        self.modelo = modelo

class Marca:
    def __init__(self, nome_marca, fornecedor):
        self.nome_marca = nome_marca
        self.fornecedor = fornecedor
    
class Transacao:
    def __init__(self, id_transacao, data_transacao, usuario, produto, id_autorizacao):
        self.id_transacao = id_transacao
        self.data_transacao = data_transacao
        self.usuario = usuario
        self.produto = produto
        self.id_autorizacao = id_autorizacao
    
class Produto:
    def __init__(self, id_produto, cor, preco: float, quantidade:int, tipo_produto,
                tamanho_produto, marca, tipo_material, ano_modelo):
        self. id_produto = id_produto
        self.cor = cor
        self.preco = preco
        self.quantidade = quantidade
        self.tipo_produto = tipo_produto
        self.tamanho_produto = tamanho_produto
        self.marca = marca
        self.tipo_material = tipo_material
        self.ano_modelo = ano_modelo
    