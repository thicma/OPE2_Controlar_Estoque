from estoque import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, send_from_directory
from estoque.models import Produto, User, Transacao, Fornecedor
from estoque.forms import RegisterForm, LoginForm, FornecedorForm
from estoque import db
from flask_login import login_user, logout_user, login_required
from datetime import datetime

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/estoque')
@login_required
def estoque_page():
    produtos = Produto.query.all()
    return render_template('estoque.html', produtos = produtos)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                            name = form.name.data,
                            charge = form.charge.data,
                            password = form.password.data)
        date_create = Transacao()
        db.session.add(user_to_create)
        db.session.add(date_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Conta criada com suecesso. Logado como usuário {user_to_create.username}', category='success')
        return redirect(url_for('estoque_page'))
    if form.errors !={}: #Se não existir erro de validação
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro para criar o usuário: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/register_fornecedor', methods=['GET', 'POST'])
def register_fornecedor():
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
        form.id.data = ""
        form.name.data = ""
        form.email.data = ""
        form.fone.data = ""
        form.cnpj.data = ""
        return render_template('register_fornecedor.html', form=form)
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro ao cadastrar o fornecedor: {err_msg}', category='danger')
    return render_template('register_fornecedor.html', form=form)

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
    image = "logo.png"
    return send_from_directory("images", image)