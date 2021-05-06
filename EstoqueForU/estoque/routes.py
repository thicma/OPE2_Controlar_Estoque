from estoque import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, send_from_directory, session, request
from estoque.models import Produto, User, Transacao, Fornecedor, Produto, Marca, Categoria
from estoque.forms import RegisterForm, LoginForm, FornecedorForm, ProdutoForm, MarcaForm, ConsultaForm
from estoque import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import or_, and_
import re
import locale
locale.setlocale(locale.LC_MONETARY, 'Portuguese_Brazil.1252')


listar_todos_produtos = Produto.query.all()
masculino = 0
feminino = 0
todos = 1

@app.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')

@app.route('/masculino', methods=['POST'])
def produtos_masculinos():
    global masculino
    global feminino
    global todos
    masculino = 1
    feminino = 0
    todos = 0
    colunas = Produto.__table__.columns.keys()
    resultado = Produto.query.filter(Produto.genero == "masculino").all()
    print(f'masculino: {masculino} | feminino: {feminino} | todos{todos}')
    return render_template('estoque.html', resultado=resultado, colunas=colunas)

@app.route('/feminino', methods=['POST'])
def produtos_feminino():
    global masculino
    global feminino
    global todos
    masculino = 0
    feminino = 1
    todos = 0
    colunas = Produto.__table__.columns.keys()
    resultado = Produto.query.filter(Produto.genero == "feminino").all()
    print(f'masculino: {masculino} | feminino: {feminino} | todos{todos}')
    return render_template('estoque.html', resultado=resultado, colunas=colunas)


"""
@app.route('/', methods=['POST'])
def busca_check():
    form = request.form
    filters = {'categoria': None ,'descricao': None,'modelo': None,'genero':form["masculino"],
            'ano_colecao':form["2020"],'material':None,'cor':None,'tamanho':form["p"]}
    
    resultado = Produto.query.filter(*filters).all()
    
    return render_template("home.html")
"""

@app.route('/estoque', methods=['GET'])
@login_required
def mostar_tela_de_estoque():
    global masculino
    global feminino
    global todos
    masculino = 0
    feminino = 0
    todos = 1
    form=ConsultaForm()
    resultado = Produto.query.all()
    colunas = Produto.__table__.columns.keys()
    colunas.pop(0)
    print(f'masculino: {masculino} | feminino: {feminino} | todos{todos}')
    return render_template('estoque.html', form=form, resultado=resultado, colunas=colunas)


def entrada_produto():
    pass
    

def saida_produto():
    pass

@app.route('/estoque', methods=['POST'])
@login_required
def estoque_page():
    global masculino
    global feminino
    global todos
    masculino = 0
    feminino = 0
    todos = 1
    session.modified = True
    form=ConsultaForm()
    resultado = ''
    print(f'masculino: {masculino} | feminino: {feminino} | todos{todos}')
    if form.validate_on_submit():
        resultado = consulta(form.consulta.data.lower())
        if resultado != False:
            return render_template('estoque.html', form=form, resultado=resultado)
        else:
            flash('Nenhum resultado encontrado!', category='info')
    return render_template('estoque.html', form=form)

def consulta(atributo_para_consulta):
    condicao = Produto.query.filter(and_(Produto.categoria_id.contains(atributo_para_consulta),
                                        Produto.tamanho_id.in_(['m','gg','g']))).all()
    if condicao :
        condicao = condicao
        return condicao
    return False
"""
                                        Produto.marca_nome.contains(atributo_para_consulta), 
                                        Produto.ano_colecao == atributo_para_consulta,
                                        Produto.material.contains(atributo_para_consulta),
                                        Produto.descricao.contains(atributo_para_consulta),
                                        Produto.id.contains(atributo_para_consulta),
                                        Produto.modelo.contains(atributo_para_consulta))).all()
"""

#consulta_dinamica(busca_valores_checkbox)
@app.route('/consulta_filtro', methods=['POST'])
def busca_valores_checkbox():
    global masculino
    global feminino
    global todos
    lista_tamanhos = request.form.getlist('tamanho')
    lista_categoria = request.form.getlist('categoria')
    resultado = ''
    if masculino == 1:
        resultado = Produto.query.filter(and_(Produto.genero == 'masculino',
                                        Produto.tamanho_id.in_(lista_tamanhos),
                                        Produto.categoria_id.in_(lista_categoria))).all()

    print(resultado)    
    return render_template('estoque.html', resultado=resultado)

def consulta_dinamica(lista_de_checkbox):
    resultado = ""
    for lista in lista_de_checkbox:
        resultado = consulta(lista)

    return resultado

@app.template_filter()
def formatar_moeda(preco):
    preco = float(preco)
    preco = locale.currency(preco,grouping=True)
    return preco

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    session.modified = True
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                            name = form.name.data,
                            charge = form.charge.data,
                            password = form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Conta criada com suecesso. Logado como usuário {user_to_create.username}', category='success')
        return redirect(url_for('estoque_page'))
    if form.errors !={}: #Se não existir erro de validação
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro para criar o usuário: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/register_fornecedor', methods=['GET', 'POST'])
@login_required
def register_fornecedor():
    session.modified = True
    form = FornecedorForm()
    if form.validate_on_submit():
        fornecedor_to_create = Fornecedor(id = form.id.data,
                                        name = form.name.data,
                                        email = form.email.data,
                                        fone = form.fone.data,
                                        cnpj = form.cnpj.data)
        db.session.add(fornecedor_to_create)
        db.session.commit()
        flash(f'Fornecedor {fornecedor_to_create.name} cadastrado com sucesso', category='sucess')
        return redirect(url_for('register_fornecedor'))
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro ao cadastrar o fornecedor: {err_msg}', category='danger')
    return render_template('register_fornecedor.html', form=form)

@app.route('/cadastrar_produto', methods=['GET'])
@login_required
def mostrar_tela_de_cadastro_do_produto():
    form=ProdutoForm()
    categorias = Produto.query.all()
    return render_template('cadastrar_produto.html', form=form, categorias=categorias)

@app.route('/cadastrar_produto', methods=['POST'])
@login_required
def cadastrar_produto():
    session.modified = True    
    form = ProdutoForm()
    validar_quantidade = validar_quantidade_informada(form.quantidade.data)
    if form.validate_on_submit():
        print(form.categoria.data)      
        if validar_preco != False and validar_preco != None:
            if validar_quantidade != False and validar_quantidade != None:
                produto_criado = Produto(tipo = form.categoria.data.lower(),
                                    descricao = form.descricao.data.lower(),
                                    modelo = form.modelo.data.lower(),
                                    ano_colecao = form.ano_colecao.data,
                                    material = form.material.data.lower(),
                                    cor = form.cor.data.lower(),
                                    preco = validar_preco,
                                    quantidade = form.quantidade.data,
                            tamanho_id = form.tamanho.data.lower(),
                            marca_nome = form.marca.data.lower()) 
                db.session.add(produto_criado)
                db.session.commit()
                flash(f'Produto {produto_criado.tipo} cadastrado com sucesso', category='success')
                return redirect(url_for("cadastrar_produto"))
            else:
                flash("Quantidade inválida! Informe apenas números inteiros.", category='danger')
                return render_template('cadastrar_produto.html', form=form, categorias=categorias)
        else:
            flash("Preço inválido! Informe apenas números positivos e separados por . ou ,", category='danger')
            return render_template('cadastrar_produto.html', form=form, categorias=categorias)
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro ao cadastrar o Produto: {err_msg}', category='danger')
    return render_template('cadastrar_produto.html', form=form, categorias=categorias)

def validar_preco_informado(preco_informado):
    preco_formatado = ''
    if re.match("^[1-9]\d{0,7}((\.|\,)\d{1,4})$",preco_informado):
        preco_formatado = preco_informado.replace(',', '.')
        return preco_formatado
    elif re.match("^[1-9]",preco_informado):
        return preco_informado
    return False

def validar_quantidade_informada(quantidade_informada):
    if re.match("[1-9]",quantidade_informada):
       return True
    return False

@app.route('/cadastrar_marca', methods=['GET', 'POST'])
@login_required
def cadastrar_marca():
    session.modified = True
    form = MarcaForm()
    if form.validate_on_submit():
        marca_criada = Marca(nome = form.nome.data,
                            fornecedor = form.fornecedor.data)
        db.session.add(marca_criada)
        db.session.commit()
        flash(f'Marca {marca_criada.nome} cadastrada com sucesso', category='sucess')
        return redirect(url_for('cadastrar_marca'))
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro ao cadastrar a Marca', category='danger')    
    return render_template('cadastrar_marca.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Sucesso! Usuário logado: {attempted_user.username}', category='success')
            session.permanent = True
            session.modified = True
            return redirect(url_for('estoque_page'))
        
        else:
            flash('Usuário e senha não correspondem! Tente novamente', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('Você foi deslogado!', category='info')
    return redirect(url_for('home_page'))

@app.route('/logo', methods=['GET'])
def logo():
    image = "logo2.png"
    return send_from_directory("images", image)