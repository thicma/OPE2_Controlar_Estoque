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
