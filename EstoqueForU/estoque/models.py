from sqlalchemy.orm.relationships import foreign
from estoque import db, login_manager
from estoque import bcrypt
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    name = db.Column(db.String(length=100), nullable=False, unique=False)
    admissao= db.Column(db.Date(), nullable=False, default=datetime.today())
    password_hash = db.Column(db.String(length=60), nullable=False)
    situacao_id = db.Column(db.Integer(), db.ForeignKey('situacao_funcionario.id'))
    situacao = relationship('SituacaoFuncionario', foreign_keys=[situacao_id])
    cargo_id = db.Column(db.Integer(), db.ForeignKey('cargos.id'))
    cargo = relationship('Cargos', foreign_keys=[cargo_id])

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
class Cargos(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    descricao = db.Column(db.String(length=20), nullable=False, unique=True)

class Categoria(db.Model)   :
    id = db.Column(db.Integer(), primary_key=True)
    descricao = db.Column(db.String(length=50), nullable=False)

    def __repr__(self):
        return f'{self.descricao}'

class Fornecedor(db.Model):
    id= db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    fone = db.Column(db.String(length=15), nullable=False, unique=False)
    cnpj = db.Column(db.String(length=14), nullable=False, unique=True)
    situacao_id = db.Column(db.Integer(), db.ForeignKey('situacao.id'))
    situacao = relationship('Situacao', foreign_keys=[situacao_id])


class Tamanho(db.Model):
    id = db.Column(db.String(length=2), primary_key=True)
    descricao = db.Column(db.String(length=15), nullable=False)

class Situacao(db.Model):
    id = id = db.Column(db.Integer(), primary_key=True)
    descricao = db.Column(db.String(length=50), nullable=False)

class SituacaoFuncionario(db.Model):
    id = id = db.Column(db.Integer(), primary_key=True)
    descricao = db.Column(db.String(length=50), nullable=False)

class Marca (db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(length=50), nullable=False)
    fornecedor_id = db.Column(db.Integer(), db.ForeignKey('fornecedor.id'))
    fornecedor = relationship('Fornecedor', foreign_keys=[fornecedor_id])
    fornecedor_id_2 = db.Column(db.Integer(), db.ForeignKey('fornecedor.id'))
    fornecedor2 = relationship('Fornecedor', foreign_keys=[fornecedor_id_2])
    fornecedor_id_3 = db.Column(db.Integer(), db.ForeignKey('fornecedor.id'))
    fornecedor3 = relationship('Fornecedor', foreign_keys=[fornecedor_id_3])
    situacao_id = db.Column(db.Integer(), db.ForeignKey('situacao.id'))
    situacao = relationship('Situacao', foreign_keys=[situacao_id])

    def __repr__(self) -> str:
        return f'{self.fornecedor_id} / {self.fornecedor.name}'

class Material(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    descricao= db.Column(db.String(length=15), nullable=False)

class HistoricoPrecos(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_produto = db.Column(db.Integer(), db.ForeignKey('produto.id'))
    produto = relationship('Produto', foreign_keys=[id_produto])
    preco = db.Column(db.Float(), db.ForeignKey('produto.preco'))
    preco_produto = relationship('Produto', foreign_keys=[preco])
    quantidade = db.Column(db.Integer(), db.ForeignKey('produto.quantidade'))
    quantidade_produto = relationship('Produto', foreign_keys=[quantidade])


class Produto(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    categoria_id = db.Column(db.Integer(), db.ForeignKey('categoria.id'))
    categoria = relationship('Categoria', foreign_keys=[categoria_id])
    descricao = db.Column(db.String(length=50), nullable=False)
    modelo = db.Column(db.String(length=20), nullable=False)
    genero = db.Column(db.String(length=9), nullable=False)
    ano_colecao = db.Column(db.String(length=4), nullable=False)
    material_id = db.Column(db.Integer(), db.ForeignKey('material.id'))
    material = relationship('Material', foreign_keys=[material_id])
    cor = db.Column(db.String(length=15), nullable=False)  
    preco = db.Column(db.Float(), nullable=False)
    quantidade = db.Column(db.Integer(), nullable=False)
    marca_id = db.Column(db.String(length=20), db.ForeignKey('marca.id'))
    marca = relationship('Marca', foreign_keys=[marca_id])
    tamanho_id = db.Column(db.String(length=2), db.ForeignKey('tamanho.id'))
    tamanho = relationship('Tamanho', foreign_keys=[tamanho_id])
    situacao_id = db.Column(db.Integer(), db.ForeignKey('situacao.id'))
    situacao = relationship('Situacao', foreign_keys=[situacao_id])

    def __repr__(self):
        return f"{self.categoria.descricao}\n{self.descricao}\n{self.modelo}\n{self.ano_colecao}"

class MovimentacaoProduto(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    user = relationship('User', foreign_keys=[user_id])
    produto_id = db.Column(db.Integer(), db.ForeignKey('produto.id'))
    produto = relationship('Produto', foreign_keys=[produto_id])
    data = db.Column(db.Date(), nullable=False, default=datetime.today())
    hora = db.Column(db.Time(timezone=True), nullable=False, default=datetime.now().time())
    quantidade = db.Column(db.Integer(), nullable=False)
    valor = db.Column(db.Float(), nullable=False)
    tipo_movimentacao = db.Column(db.String(length=10), nullable=False)
    

    

