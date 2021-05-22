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
    charge= db.Column(db.String(length=50), nullable=False, unique=False)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    

class Categoria(db.Model)   :
    id = db.Column(db.Integer(), primary_key=True)
    descricao = db.Column(db.String(length=50), nullable=False)

    def __repr__(self):
        return f'{self.descricao}'

class Autorizacao_Velha(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    descricao = db.Column(db.String(15))

    def __repr__(self):
        return f"ID: {self.id}\n{self.descricao}"


class Fornecedor(db.Model):
    id= db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    fone = db.Column(db.String(length=15), nullable=False, unique=False)
    cnpj = db.Column(db.String(length=14), nullable=False, unique=True)


class Tamanho(db.Model):
    id = db.Column(db.String(length=2), primary_key=True)
    descricao = db.Column(db.String(length=15), nullable=False)

class Marca (db.Model):
    nome = db.Column(db.String(length=20), primary_key=True)
    id = db.Column(db.Integer(), autoincrement=True, nullable=False)
    fornecedor = db.Column(db.Integer(), nullable=False)

class Material(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    descricao= db.Column(db.String(length=15), nullable=False)

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

    def __repr__(self):
        return f"{self.categoria.descricao}\n{self.descricao}\n{self.modelo}\n{self.ano_colecao}"
class Autorizacao(db.Model):
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
    

    

