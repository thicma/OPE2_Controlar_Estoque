from estoque import db, login_manager
from estoque import bcrypt
from flask_login import UserMixin
from sqlalchemy import DateTime, or_
from datetime import datetime, timezone
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
    transcao = db.relationship('Transacao', backref='transacao')

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Tipo(db.Model)   :
    id = db.Column(db.Integer(), primary_key=True)
    descricao = db.Column(db.String(length=50), nullable=False)
    material = db.Column(db.String(length=20), nullable=False)
    modelo= db.Column(db.String(length=20), nullable=False)
    ano_colecao = db.Column(db.Integer(), nullable=False)

class Autorizacao(db.Model):
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
    fornecedor= db.Column(db.Integer(), nullable=False)


class Produto(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    tipo = db.Column(db.String(length=15), nullable=False)
    descricao = db.Column(db.String(length=50), nullable=False)
    modelo = db.Column(db.String(length=20), nullable=False)
    ano_colecao = db.Column(db.Integer(), nullable=False)
    material = db.Column(db.String(length=20), nullable=False)
    cor = db.Column(db.String(length=15), nullable=False)    
    preco = db.Column(db.Float(), nullable=False)
    quantidade = db.Column(db.Integer(), nullable=False)
    marca_nome = db.Column(db.String(length=20), db.ForeignKey('marca.nome'))
    marca = relationship('Marca', foreign_keys=[marca_nome])
    tamanho_id = db.Column(db.String(length=2), db.ForeignKey('tamanho.id'))
    tamanho = relationship('Tamanho', foreign_keys=[tamanho_id])

    def __repr__(self):
        return f"{self.id}\n{self.tipo}\n{self.descricao}"

class Transacao(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    data = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    produto_id = db.Column(db.Integer(), db.ForeignKey('produto.id'))
    user = relationship('User', foreign_keys=[user_id])
    produto = relationship('Produto', foreign_keys=[produto_id])
    
    

    def __repr__(self):
        return f"{self.id}\n{self.data}"
