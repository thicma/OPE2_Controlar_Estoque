from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
#from wtforms.fields.core import DateField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from estoque.models import *


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Usuário já existe! Por favor, tente cadastrar um usuário diferente.')  

    username = StringField(label='Usuário:', validators=[Length(min=2, max=30), DataRequired()])
    name = StringField(label='Nome Completo', validators=[Length(min=2, max=50), DataRequired()])
    charge = StringField(label='Cargo: ', validators=[Length(min=2, max=15), DataRequired()])
    password = PasswordField(label='Senha:', validators=[Length(min=6), DataRequired()])
    password_confirm = PasswordField(label='Confirmar Senha:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Criar Usuário')

class LoginForm (FlaskForm):
    username = StringField(label='Usuário:', validators=[DataRequired()])
    password = PasswordField(label='Senha:', validators=[DataRequired()])
    submit = SubmitField(label='Entrar')

class FornecedorForm(FlaskForm):

    def validate_id(self, id_to_check):
        id = Fornecedor.query.filter_by(id=id_to_check.data).first()
        if id:
            raise ValidationError(f'Código de fornecedor já registrado para o Fornecedor {id.name}')

    def validate_fornecedor(self, fornecedor_to_check):
        name = Fornecedor.query.filter_by(name=fornecedor_to_check.data).first()
        if name:
            raise ValidationError(f'{name.name} já registrado com o código {name.id}')

    def validate_cnpj(self, cnpj_to_check):
        cnpj = Fornecedor.query.filter_by(cnpj=cnpj_to_check.data).first()
        if cnpj:
            raise ValidationError(f'{cnpj.cnpj} já registrado com o código {cnpj.id}')

    def validate_email(self, email_to_check):
        email = Fornecedor.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError(f'{email.email} já registrado com o código {email.id}')    

    id = StringField(label='Código Fornecedor: ', validators=[Length(min=2, max=10), DataRequired()])
    name = StringField(label='Fornecedor:', validators=[Length(min=2, max=50), DataRequired()])
    email = StringField(label='E-mail:', validators=[Length(min=2, max=30), DataRequired()])
    fone = StringField(label='Telefone:', validators=[Length(min=2, max=30), DataRequired()])
    cnpj = StringField(label='CNPJ:', validators=[Length(min=14, max=14), DataRequired()])
    submit = SubmitField(label='Cadastrar')  


def seleciona_categoria():
    categorias= Categoria.query.all()
    lista_de_categoria = [(categoria.id, categoria.descricao.title()) for categoria in categorias]
    return lista_de_categoria

def seleciona_marca():
    marcas = Marca.query.all()
    lista_de_marcas = [(marca.id, marca.nome.title()) for marca in marcas]
    return lista_de_marcas

def seleciona_material():
    materiais = Material.query.all()
    lista_de_materiais = [(material.id, material.descricao.title()) for material in materiais]
    return lista_de_materiais

def seleciona_tamanho():
    tamanhos = Tamanho.query.all()
    lista_de_tamanhos = [(tamanho.id, tamanho.id.upper()) for tamanho in tamanhos]
    return lista_de_tamanhos

class SelecionaDataForm(FlaskForm):
    data_inicial = DateField('Data Inicial', format='%Y-%m-%d')
    data_final = DateField('Data Final', format='%Y-%m-%d')

class AtualizacaoForm(FlaskForm):
    descricao = StringField(label='Descrição do Produto', validators=[Length(max=50), DataRequired()])
    ano_colecao = StringField(label='Ano da Colecao', validators=[Length(min=4, max=4), DataRequired()])
    tamanho = SelectField(u'Tamanho', choices = seleciona_tamanho())
    categorias = SelectField(u'Categoria', choices=seleciona_categoria())
    modelo = StringField(label='Modelo', validators=[Length(max=20), DataRequired()]) 
    genero = SelectField('genero', choices = [('feminino','Feminino'), ('masculino','Masculino')])
    material = SelectField(u'Material', choices = seleciona_material())
    cor = StringField(label='Cor do Produto', validators=[Length(max=15), DataRequired()])
    marcas = SelectField(u'Marca', choices = seleciona_marca())
    submit = SubmitField(label='Confirmar')


class ProdutoForm(FlaskForm):    
    categoria = SelectField(u"Categoria", choices=seleciona_categoria())
    descricao = StringField(label='Descrição do Produto', validators=[Length(max=50), DataRequired()])
    modelo = StringField(label='Modelo', validators=[Length(max=20), DataRequired()])
    genero = SelectField(u"Genero", choices=[('f','feminino'),('m','masculino')])
    ano_colecao = StringField(label='Ano da Colecao', validators=[Length(min=4, max=4), DataRequired()])
    material = StringField(label='Material', validators=[Length(max=20), DataRequired()])
    cor = StringField(label='Cor do Produto', validators=[Length(max=15), DataRequired()])
    preco = StringField(label='Valor Unitário', validators=[DataRequired()])
    quantidade = StringField(label='Quantidade', validators=[DataRequired()])
    tamanho = SelectField(u"Tamanho", choices=[(tamanho.id, tamanho.descricao) for tamanho in Tamanho.query.all()])
    marca = StringField(label='Marca', validators=[Length(max=20), DataRequired()])
    submit = SubmitField(label='Cadastrar Produto')

class MarcaForm(FlaskForm):
    nome = StringField(label='Marca', validators=[Length(max=20), DataRequired()])
    fornecedor = StringField(label='Fornecedor', validators=[DataRequired()])
    submit = SubmitField(label='Cadastrar Marca')

class ConsultaForm(FlaskForm):
    consulta = StringField(label='Produto a consultar:', validators=[DataRequired()])
    submit = SubmitField(label='Consultar')