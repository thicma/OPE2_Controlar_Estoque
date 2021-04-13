from estoque import db, login_manager
from estoque import bcrypt
from flask_login import UserMixin
from sqlalchemy import DateTime
import datetime


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

class Item(db.Model):
    id= db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Float(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'
    
"""
class Autorizacao(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    descricao = db.Column(db.String(15))
"""
class Transacao(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    data = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
"""
class Fornecedor(db.Model):
    pass

class Tipo_Produto(db.Model):
    pass

class Tamanho(db.Model):
    pass

class Marca (db.Model):
    pass
"""
