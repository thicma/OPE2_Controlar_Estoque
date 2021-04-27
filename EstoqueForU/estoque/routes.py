from estoque import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, send_from_directory, session, request
from estoque.models import Produto, User, Transacao, Fornecedor, Produto, Marca, Tipo
from estoque.forms import RegisterForm, LoginForm, FornecedorForm, ProdutoForm, MarcaForm, TipoForm, ConsultaForm
from estoque import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import or_

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/estoque', methods=['GET'])
@login_required
def mostar_tela_de_estoque():
    form=ConsultaForm()
    resultado = Produto.query.all()
    return render_template('estoque.html', form=form, resultado=resultado)

@app.route('/estoque', methods=['POST'])
@login_required
def estoque_page():
    session.modified = True
    form=ConsultaForm()
    transacao = None
    resultado = ''
    if form.validate_on_submit():
        resultado = consulta(form.consulta.data.lower())
        transacao = registra_transacao(form.consulta.data)
        if resultado != False:
            return render_template('estoque.html', form=form, resultado=resultado)
        else:
            flash('Nenhum resultado encontrado!', category='info')
    return render_template('estoque.html', form=form)

def consulta(atributo_para_consulta):
    condicao = Produto.query.filter(or_(Produto.tipo.contains(atributo_para_consulta), Produto.tamanho_id == atributo_para_consulta,
                                     Produto.marca_nome.contains(atributo_para_consulta), Produto.ano_colecao == atributo_para_consulta,
                                     Produto.material.contains(atributo_para_consulta),Produto.descricao.contains(atributo_para_consulta))).all()
    if condicao :
        condicao = condicao
        return condicao
    return False

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
        form.id.data = None
        form.name.data = None
        form.email.data = None
        form.fone.data = None
        form.cnpj.data = None
        return render_template('register_fornecedor.html', form=form)
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro ao cadastrar o fornecedor: {err_msg}', category='danger')
    return render_template('register_fornecedor.html', form=form)

@app.route('/cadastrar_produto', methods=['GET'])
@login_required
def mostrar_tela_de_cadastro_do_produto():
    form=ProdutoForm()
    return render_template('cadastrar_produto.html', form=form)

@app.route('/cadastrar_produto', methods=['POST'])
@login_required
def cadastrar_produto():
    session.modified = True    
    form = ProdutoForm()
    validar_preco = validar_preco_informado(form.preco.data)
    if form.validate_on_submit():
            produto_criado = Produto(tipo = form.tipo.data.lower(),
                                    descricao = form.descricao.data.lower(),
                                    modelo = form.modelo.data.lower(),
                                    ano_colecao = form.ano_colecao.data,
                                    material = form.material.data.lower(),
                                    cor = form.cor.data.lower(),
                                    preco = validar_preco,
                                    quantidade = form.quantidade.data,
                                    tamanho_id = form.tamanho.data.upper(),
                                    marca_nome = form.marca.data.lower()) 
            db.session.add(produto_criado)
            db.session.commit()
            flash(f'Produto {produto_criado.tipo} cadastrado com sucesso', category='sucess')
            form.tipo.data = None
            form.descricao.data = None
            form.modelo.data = None     
            form.ano_colecao.data = None
            form.material.data = None
            form.cor.data = None
            form.preco.data = None
            form.quantidade.data = None
            form.tamanho.data = None
            form.marca.data = None
            return render_template('cadastrar_produto.html', form=form)
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro ao cadastrar o Produto: {err_msg}', category='danger')
    return render_template('cadastrar_produto.html', form=form)

def validar_preco_informado(preco_informado):
    preco_formatado = ''
    if ',' in preco_informado:
        preco_formatado = preco_informado.replace(',', '.')
        return preco_formatado
    return preco_informado
        


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
        form.nome.data = None
        form.fornecedor.data = None
        return render_template('cadastrar_marca.html', form=form)
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro ao cadastrar a Marca', category='danger')    
    return render_template('cadastrar_marca.html', form=form)

@app.route('/cadastrar_tipo', methods=['GET', 'POST'])
def cadastrar_tipo():
    session.modified = True
    form = TipoForm()
    if form.validate_on_submit():
        tipo_criado = Tipo(id = form.id.data,
                            descricao = form.descricao.data,
                            material = form.material.data,
                            modelo = form.modelo.data,
                            ano_colecao = form.ano_colecao.data
                            )
        db.session.add(tipo_criado)
        db.session.commit()
        flash(f'Tipo {tipo_criado.id} - {tipo_criado.descricao} criado com sucesso.', category='sucess')
        form.id.data = None
        form.descricao.data = None
        form.material.data = None
        form.modelo.data = None
        form.ano_colecao.data = None
        return redirect(url_for('cadastrar_produto'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro ao cadastrar o Tipo do Produto: {err_msg}', category='danger')
    return render_template('cadastrar_tipo.html', form=form)

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

def registra_transacao(produto):
    transacao = Transacao(user_id = current_user.id,
                        produto_id = produto)
    db.session.add(transacao)
    db.session.commit()
    return True

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('Você foi deslogado!', category='info')
    return redirect(url_for('home_page'))

@app.route('/logo', methods=['GET'])
def logo():
    image = "logo2.png"
    return send_from_directory("images", image)