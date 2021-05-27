from operator import methodcaller
from os import abort
from sqlalchemy.orm.session import Session
from estoque import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, send_from_directory, session, request
from estoque.models import Produto, User, Material, Fornecedor, Produto, Marca, Categoria, Tamanho, Autorizacao
from estoque.forms import RegisterForm, LoginForm, FornecedorForm, ProdutoForm, MarcaForm, ConsultaForm, AtualizacaoForm, SelecionaDataForm
from estoque import db
from estoque.gerar_pdf import *
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, timedelta
from sqlalchemy import or_, and_
import re, os
import os.path


def gera_nome_colunas():
    return ['Categoria','Descrição','Modelo','Gênero','Ano da Coleção','Material','Cor','Preço','Quantidade','Nome da Marca','Tamanho']

def gera_label_para_checkbox_categoria():
    categorias = Categoria.query.all()
    categoria_label_checkbox = [(categoria.id, categoria.descricao) for categoria in categorias]
    return categoria_label_checkbox

def gera_label_para_checkbox_ano_colecao():
    ano_colecao = Produto.query.all()
    ano_label_para_checkbox = []
    for ano in ano_colecao:
        if ano.ano_colecao not in ano_label_para_checkbox:
            ano_label_para_checkbox.append(ano.ano_colecao)
    ano_label_para_checkbox.sort()
    return ano_label_para_checkbox

def gera_label_para_checkbox_material():
    materiais = Material.query.all()
    material_label_checkbox = [(material.id, material.descricao) for material in materiais]
    return material_label_checkbox

def gera_label_para_checkbox_marca():
    marcas = Marca.query.all()
    marca_label_checkbox = [(marca.id, marca.nome) for marca in marcas]
    marca_label_checkbox.sort()
    return marca_label_checkbox


@app.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')

@app.route('/estoque', methods=['GET'])
@login_required
def mostar_tela_de_estoque():
    form=ConsultaForm()
    resultado = Produto.query.all()
    atualiza_form = AtualizacaoForm()
    colunas = gera_nome_colunas()
    label_categoria = gera_label_para_checkbox_categoria()
    label_ano=gera_label_para_checkbox_ano_colecao()
    label_marca = gera_label_para_checkbox_marca()
    label_material = gera_label_para_checkbox_material()
    return render_template('estoque.html', form=form, resultado=resultado, colunas=colunas, label_categoria=label_categoria, 
                           label_ano=label_ano, label_marca=label_marca, label_material=label_material, atualiza_form = atualiza_form)

@app.route('/estoque', methods=['POST'])
@login_required
def estoque_page():
    atualiza_form = AtualizacaoForm()
    session.modified = True
    resultado = ''
    colunas = gera_nome_colunas()
    label_categoria = gera_label_para_checkbox_categoria()
    label_ano=gera_label_para_checkbox_ano_colecao()
    label_marca = gera_label_para_checkbox_marca()
    label_material = gera_label_para_checkbox_material()
    resultado = consulta(request.form['consultar'].lower())
    if resultado != False:
        return render_template('estoque.html', resultado=resultado, colunas=colunas, label_categoria=label_categoria, 
                           label_ano=label_ano, label_marca=label_marca, label_material=label_material, genero="", atualiza_form=atualiza_form)
    else:
        flash('Nenhum resultado encontrado!', category='info')
    return render_template('estoque.html')

@app.route('/masculino', methods=['POST'])
@login_required
def produtos_masculinos():
    session.modified = True
    atualiza_form = AtualizacaoForm()
    colunas = gera_nome_colunas()
    label_categoria = gera_label_para_checkbox_categoria()
    label_ano=gera_label_para_checkbox_ano_colecao()
    label_marca = gera_label_para_checkbox_marca()
    label_material = gera_label_para_checkbox_material()
    resultado = Produto.query.filter(Produto.genero == "masculino").all()
    return render_template('estoque.html', resultado=resultado, colunas=colunas, label_categoria=label_categoria, 
                           label_ano=label_ano, label_marca=label_marca, label_material=label_material, genero="masculino", atualiza_form=atualiza_form)

@app.route('/feminino', methods=['POST'])
@login_required
def produtos_feminino():
    session.modified = True
    atualiza_form = AtualizacaoForm()
    colunas = gera_nome_colunas()
    label_categoria = gera_label_para_checkbox_categoria()
    label_ano=gera_label_para_checkbox_ano_colecao()
    label_marca = gera_label_para_checkbox_marca()
    label_material = gera_label_para_checkbox_material()
    resultado = Produto.query.filter(Produto.genero == "feminino").all()
    return render_template('estoque.html', resultado=resultado, colunas=colunas, label_categoria=label_categoria, 
                           label_ano=label_ano, label_marca=label_marca, label_material=label_material, genero="feminino", atualiza_form=atualiza_form)

#==========================================================================================================

@app.route('/entrada_produto', methods=['POST'])
@login_required
def mostra_tela_de_entrada():
    flash('Para ajuste de preço do produto: Deixe a quantidade em 0 (ZERO) e modifique o preço!')
    id_produto = int(request.form['produto'])
    produto = Produto.query.filter_by(id=id_produto).first()
    return render_template('entrada_produto.html', produto=produto, id_produto=id_produto)

@app.route('/registra_entrada_produto', methods=['POST'])
@login_required
def entrada_produto():
    session.modified = True
    registra_movimentacao = ''
    id_produto = int(request.form['produto'])
    produto = Produto.query.filter_by(id=id_produto).first()
    quantidade_da_entrada = validar_quantidade_informada(request.form['quantidade_entrada'])
    preco_do_produto = validar_preco_informado(request.form['preco'])
    print(preco_do_produto)

    if quantidade_da_entrada >= 0:
        if preco_do_produto != produto.preco and quantidade_da_entrada == 0:
            valor_ajuste = (produto.quantidade * preco_do_produto)
            registra_movimentacao = Autorizacao(user_id = current_user.id,
                                                        produto_id = id_produto,
                                                        quantidade = produto.quantidade,
                                                        valor = valor_ajuste,
                                                        tipo_movimentacao = 'ajuste')
            produto.preco = preco_do_produto
            soma_da_entrada = produto.quantidade + quantidade_da_entrada
            produto.quantidade = soma_da_entrada
            db.session.add(registra_movimentacao)
            db.session.commit()
            flash('Ajuste de preço realizado com sucesso!', category="success")
            return redirect(url_for('mostar_tela_de_estoque'))
        elif preco_do_produto == produto.preco and quantidade_da_entrada > 0:
            registra_movimentacao = Autorizacao(user_id = current_user.id,
                                                        produto_id = id_produto,
                                                        quantidade = quantidade_da_entrada,
                                                        valor = quantidade_da_entrada * produto.preco,
                                                        tipo_movimentacao = 'entrada')
            produto.preco = preco_do_produto
            soma_da_entrada = produto.quantidade + quantidade_da_entrada
            produto.quantidade = soma_da_entrada
            db.session.add(registra_movimentacao)
            db.session.commit()
            flash('Entrada efetuada com sucesso!', category="success")
            return redirect(url_for('mostar_tela_de_estoque'))
        elif preco_do_produto != produto.preco and quantidade_da_entrada != produto.quantidade:
            registra_movimentacao = Autorizacao(user_id = current_user.id,
                                                        produto_id = id_produto,
                                                        quantidade = quantidade_da_entrada,
                                                        valor = (quantidade_da_entrada * preco_do_produto) + ((preco_do_produto - produto.preco) * produto.quantidade),
                                                        tipo_movimentacao = 'entrada com ajuste')
            produto.preco = preco_do_produto
            soma_da_entrada = produto.quantidade + quantidade_da_entrada
            produto.quantidade = soma_da_entrada
            db.session.add(registra_movimentacao)
            db.session.commit()
            flash('Entrada efetuada com sucesso!', category="success")
            return redirect(url_for('mostar_tela_de_estoque'))
        else:
            flash('A entrada deve ser realizada apenas com números e positivos!',category='danger')        
    else:
        flash('A quantidade de entrada deve ser positiva ou 0 para ajuste de preço!')
    return render_template('entrada_produto.html', produto=produto, id_produto=id_produto)

# ===========================================================================================================

@app.route('/saida_produto', methods=['POST'])
@login_required
def mostra_tela_de_saida():
    flash('Para ajuste de preço do produto: Deixe a quantidade em 0 (ZERO) e modifique o preço!')
    id_produto = int(request.form['produto'])
    produto = Produto.query.filter_by(id=id_produto).first()
    return render_template('saida_produto.html', produto=produto, id_produto=id_produto)

@app.route('/registra_saida_produto', methods=['POST'])
@login_required
def saida_produto():
    session.modified = True
    id_produto = int(request.form['produto'])
    produto = Produto.query.filter_by(id=id_produto).first()
    quantidade_da_saida = validar_quantidade_informada(request.form['quantidade_saida'])
    preco_do_produto = validar_preco_informado(request.form['preco'])    
    if quantidade_da_saida:
        saida_do_produto = produto.quantidade - quantidade_da_saida
        if saida_do_produto >= 0:
            if preco_do_produto != produto.preco and quantidade_da_saida == 0:
                registra_movimentacao = Autorizacao(user_id = current_user.id,
                                                        produto_id = id_produto,
                                                        quantidade = produto.quantidade,
                                                        valor = preco_do_produto * produto.preco,
                                                        tipo_movimentacao = 'ajuste')
                produto.quantidade = saida_do_produto
                produto.preco = preco_do_produto
                db.session.add(registra_movimentacao)
                db.session.commit()
                flash('Ajuste de preço realizado com sucesso!', category="success")
                return redirect(url_for('mostar_tela_de_estoque'))
            elif preco_do_produto == produto.preco and quantidade_da_saida > 0:
                registra_movimentacao = Autorizacao(user_id = current_user.id,
                                                            produto_id = id_produto,
                                                            quantidade = quantidade_da_saida,
                                                            valor = quantidade_da_saida * preco_do_produto,
                                                            tipo_movimentacao = 'saída')
                produto.quantidade = saida_do_produto
                produto.preco = preco_do_produto
                db.session.add(registra_movimentacao)
                db.session.commit()
                flash('Saída efetuada com sucesso!', category="success")
                return redirect(url_for('mostar_tela_de_estoque'))
            elif preco_do_produto != produto.preco and quantidade_da_saida > 0:
                registra_movimentacao = Autorizacao(user_id = current_user.id,
                                            produto_id = id_produto,
                                            quantidade = quantidade_da_saida,
                                            valor = (quantidade_da_saida * preco_do_produto) + ((preco_do_produto - produto.preco) * produto.quantidade),
                                            tipo_movimentacao = 'saída com ajuste')
                produto.quantidade = saida_do_produto
                produto.preco = preco_do_produto
                db.session.add(registra_movimentacao)
                db.session.commit()
                flash('Saída efetuada com sucesso!', category="success")
                return redirect(url_for('mostar_tela_de_estoque'))
            else:
                flash('Nenhuma alteração efetuada!', category='danger')
        else:
            flash('Verifique o estoque, saída maior que o total disponível!',category='danger')
    else:
        flash('A saída deve ser realizada apenas com números e positivos!',category='danger')
    return render_template('saida_produto.html', produto=produto, id_produto=id_produto)

@app.route('/mostra_tela_de_atualizacao', methods=['POST'])
@login_required
def mostra_tela_de_atualizacao():
    id_produto = int(request.form['id_produto'])
    produto = Produto.query.filter_by(id=id_produto).first()
    atualiza_form = AtualizacaoForm(descricao=produto.descricao.title(), ano_colecao=produto.ano_colecao,
                        categorias=produto.categoria_id,modelo=produto.modelo.title(), cor=produto.cor.title(),
                        tamanho=produto.tamanho_id, marcas=produto.marca_id,
                        genero = produto.genero.title(), material=produto.material_id)
    return render_template('atualiza_produto.html', produto=produto, id_produto=id_produto, atualiza_form=atualiza_form)


@app.route('/atualiza_produto', methods=['GET','POST'])
@login_required
def atualiza_produto():
    session.modified = True
    atualiza_form = AtualizacaoForm()
    produto = Produto.query.filter_by(id=request.form['id_produto']).first()
    produto.descricao = atualiza_form.descricao.data.lower()
    produto.ano_colecao = atualiza_form.ano_colecao.data
    produto.tamanho_id = atualiza_form.tamanho.data
    produto.categoria_id = atualiza_form.categorias.data
    produto.modelo = atualiza_form.modelo.data.lower()
    produto.genero = atualiza_form.genero.data
    produto.material_id = atualiza_form.material.data
    produto.cor = atualiza_form.cor.data.lower()
    produto.marca_id = atualiza_form.marcas.data
    db.session.commit()
    flash(f'Produto {produto.id} - {produto.descricao} alterado com sucesso', category='success')
    return redirect(url_for('mostar_tela_de_estoque'))

@app.route('/relatorio_movimentacao', methods=['GET'])
@login_required
def mostra_tela_relatorio_movimentacao():
    gera_nome_colunas_movimentacao = ['Produto','Marca', 'Usuário', 'Data da Movimentação', 'Quantidade', 'Valor', 'Tipo da Movimentação']
    produto=Produto.query.all()
    ultimos_trinta_dias = (date.today()) - timedelta(days=30)
    form = SelecionaDataForm(data_inicial=ultimos_trinta_dias, data_final=date.today())
    label_categoria = gera_label_para_checkbox_categoria()
    label_marca = gera_label_para_checkbox_marca()
    return render_template('relatorio_movimentacao.html', label_categoria=label_categoria, 
                           label_marca=label_marca, produto=produto, form=form, colunas=gera_nome_colunas_movimentacao, compras=0, vendas=0, ajuste=0)

@app.route('/relatorio_movimentacao', methods=['GET','POST'])
@login_required
def relatorio_movimentacao():
    session.modified = True
    gera_nome_colunas_movimentacao = ['Produto','Marca', 'Usuário', 'Data da Movimentação', 'Quantidade', 'Valor', 'Tipo da Movimentação']
    produto=Produto.query.all()
    form = SelecionaDataForm()
    label_categoria = gera_label_para_checkbox_categoria()
    label_marca = gera_label_para_checkbox_marca()
    data_inicial = form.data_inicial.data
    data_final = form.data_final.data
    hoje = date.today()
    lista_categoria = request.form.getlist('categoria')
    lista_marca = request.form.getlist('marca')
    lista_movimentacao = request.form.getlist('movimento')
    vendas = 0
    compras = 0
    ajuste = 0
    nome_do_arquivo = ""
    if data_final > hoje:
        flash('A data final da pesquisa não pode ser maior que a data atual!', category='info')
        return redirect(url_for('mostra_tela_relatorio_movimentacao'))
    elif data_inicial > data_final:
        flash('A data inicial da pesquisa não pode ser maior que a final!', category='info')
        return redirect(url_for('mostra_tela_relatorio_movimentacao'))
    if len(lista_categoria) == 0:
        lista_categoria = [(categoria.id) for categoria in Categoria.query.all()]
    if len(lista_marca) == 0:
        lista_marca = [(marca.id) for marca in Marca.query.all()]
    if len(lista_movimentacao) == 0:
        lista_movimentacao = ['ajuste','entrada','entrada com ajuste','saída', 'saída com ajuste']
    
    produtos_movimentados = Autorizacao.query.filter(and_(Autorizacao.data.between(data_inicial, data_final),
                                                        Autorizacao.produto.has(Produto.categoria_id.in_(lista_categoria)),
                                                        Autorizacao.produto.has(Produto.marca_id.in_(lista_marca)),
                                                        Autorizacao.tipo_movimentacao.in_(lista_movimentacao))).all()
    
    if len(produtos_movimentados) > 0:
        for produto in produtos_movimentados:
            if produto.tipo_movimentacao == 'saída':
                vendas += produto.valor
            elif produto.tipo_movimentacao == 'entrada':
                compras += produto.valor
            elif produto.tipo_movimentacao == 'entrada com ajuste':
                compras += produto.valor
            elif produto.tipo_movimentacao == 'saída com ajuste':
                vendas += produto.valor
            else:
                ajuste += produto.valor
        pdf = PDF('L','mm','A4')
        nome_do_arquivo = pdf.body(produtos_movimentados)

    else:
        flash('Nenhum produto resultado encontrado!', category='info')
    return render_template('relatorio_movimentacao.html', label_categoria=label_categoria, 
                           label_marca=label_marca, produtos_movimentados=produtos_movimentados, form=form, 
                           colunas=gera_nome_colunas_movimentacao, compras=compras, vendas=vendas, ajuste=ajuste, nome_do_arquivo=nome_do_arquivo)

@app.route('/relatorio_pdf/<arquivo>')
def gerar_pdf(arquivo):
    try:
        leitura_do_arquivo = send_from_directory(app.config['CLIENT_PDF'],
                                    arquivo,
                                    as_attachment=True)
        para_apagar_arquivo = apagar_arquivo(arquivo)
        return leitura_do_arquivo
                                    
    except FileNotFoundError:
        flash('Nenhum arquivo encontrado.')
        return redirect(url_for('relatorio_movimentacao'))

def apagar_arquivo(nome_do_arquivo):

    caminho = f'arquivos/{nome_do_arquivo}'
    pasta_raiz = os.getcwd()
    print(pasta_raiz)
    print(caminho)
    caminho_formatado = os.path.join(f"{app.config['CLIENT_PDF']}/",nome_do_arquivo)
    print(caminho_formatado)
    if caminho_formatado == caminho:
        print("1")
        os.chdir(f"estoque/{os.path.join(app.config['CLIENT_PDF'])}")
        for arquivo in os.listdir('.'):
            if os.path.isfile(arquivo):
                if arquivo != nome_do_arquivo:
                    print('seria removido')
        os.chdir(pasta_raiz)

        return True
    else:
        print('não deu certo')
        return False
    return False



def consulta(atributo_para_consulta):
    condicao = Produto.query.filter(or_(Produto.categoria.has(Categoria.descricao.contains(atributo_para_consulta)),
                                        Produto.tamanho_id.contains(atributo_para_consulta),
                                        Produto.marca.has(Marca.nome.contains(atributo_para_consulta)), 
                                        Produto.ano_colecao.contains(atributo_para_consulta),
                                        Produto.material.has(Material.descricao.contains(atributo_para_consulta)),
                                        Produto.descricao.contains(atributo_para_consulta),
                                        Produto.modelo.contains(atributo_para_consulta))).all()
    if condicao :
        return condicao
    return False


#consulta_dinamica(busca_valores_checkbox)
@app.route('/consulta_filtro', methods=['POST'])
@login_required
def busca_valores_checkbox():
    session.modified = True
    atualiza_form = AtualizacaoForm()
    lista_tamanhos = request.form.getlist('tamanho')
    lista_categoria = request.form.getlist('categoria')
    lista_ano_colecao = request.form.getlist('ano')
    lista_marca = request.form.getlist('marca')
    lista_material = request.form.getlist('material')
    genero = request.form['genero']

    colunas = gera_nome_colunas()
    label_categoria = gera_label_para_checkbox_categoria()
    label_ano=gera_label_para_checkbox_ano_colecao()
    label_marca = gera_label_para_checkbox_marca()
    label_material = gera_label_para_checkbox_material()
    if len(lista_categoria) == 0:
        lista_categoria = [(categoria.id) for categoria in Categoria.query.all()]
    if len(lista_tamanhos) == 0:
        lista_tamanhos = [(tamanho.id) for tamanho in Tamanho.query.all()]
    if len(lista_ano_colecao) == 0:
        lista_ano_colecao = [(str(ano.ano_colecao)) for ano in Produto.query.all()]
    if len(lista_marca) == 0:
        lista_marca = [(marca.id) for marca in Marca.query.all()]
    if len(lista_material) == 0:
        lista_material = [(material.id) for material in Material.query.all()]
    
    resultado = ''
    if genero != "":
        resultado = Produto.query.filter(and_(Produto.genero == genero,
                                        Produto.categoria_id.in_(lista_categoria),
                                        Produto.tamanho_id.in_(lista_tamanhos),
                                        Produto.material_id.in_(lista_material),
                                        Produto.marca_id.in_(lista_marca),
                                        Produto.ano_colecao.in_(lista_ano_colecao))).all()
    else:
        resultado = Produto.query.filter(and_(Produto.tamanho_id.in_(lista_tamanhos),
                                        Produto.categoria_id.in_(lista_categoria),
                                        Produto.material_id.in_(lista_material),
                                        Produto.marca_id.in_(lista_marca),
                                        Produto.ano_colecao.in_(lista_ano_colecao))).all()
    
    if len(resultado) == 0:
        flash('Nenhum produto encontrado', category='info')
 
    return render_template('estoque.html', resultado=resultado, colunas=colunas, label_categoria=label_categoria, 
                           label_ano=label_ano, label_marca=label_marca, label_material=label_material, genero=genero, atualiza_form=atualiza_form)

def consulta_dinamica(lista_de_checkbox):
    resultado = ""
    for lista in lista_de_checkbox:
        resultado = consulta(lista)
    return resultado

@app.template_filter()
def formatar_moeda(preco):
    preco = float(preco)
    a = f'{preco:,.2f}'
    b = a.replace(',','v')
    c = b.replace('.',',')
    preco = c.replace('v','.')
    return f'R${preco}'

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
    categorias = [(categoria.descricao) for categoria in Categoria.query.all()]
    validar_quantidade = validar_quantidade_informada(form.quantidade.data)
    validar_produto = verificar_se_produto_cadastrado(form.categoria.data.lower(),form.modelo.data.lower(), 
                                                        form.genero.data.lower(), form.ano_colecao.data,
                                                        form.material.data.lower(), form.cor.data.lower(), 
                                                        form.marca.data.lower(), form.tamanho.data.lower())
    if form.validate_on_submit():        
        if validar_preco != False and validar_preco != None:
            if validar_quantidade != False and validar_quantidade != None:
                if validar_produto != False:
                    produto_criado = Produto(categoria_id = form.categoria.data.lower(),
                                        descricao = form.descricao.data.lower(),
                                        modelo = form.modelo.data.lower(),
                                        ano_colecao = form.ano_colecao.data,
                                        material_id = form.material.data.lower(),
                                        cor = form.cor.data.lower(),
                                        preco = validar_preco,
                                        quantidade = validar_quantidade,
                                        tamanho_id = form.tamanho.data.lower(),
                                        marca_id = form.marca.data.lower()) 
                    db.session.add(produto_criado)
                    db.session.commit()
                    flash(f'Produto {produto_criado.tipo} cadastrado com sucesso', category='success')
                    return redirect(url_for("cadastrar_produto"))
                else:
                    flash("Produto já cadastrado.", category='danger')
                    return render_template('cadastrar_produto.html', form=form, categorias=categorias)
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
    if 'R$ ' in preco_informado:
        preco_informado = preco_informado.replace('R$ ','')
    if re.match("^[1-9]\d{0,7}((\.|\,)\d{1,4})$",preco_informado):
        preco_formatado = preco_informado.replace(',', '.')
        return float(preco_formatado)
    elif re.match("^[1-9]",preco_informado):
        return float(preco_informado)
    return False

def validar_quantidade_informada(quantidade_informada):
	try:
		val=int(quantidade_informada)
		if (val>=0):
			return val
	except:
		pass
	return False    

def validar_texto(texto_informado):
	if (texto_informado.replace(" ","").isalpha()):
		return True
	else:
		return False
    
def verificar_se_produto_cadastrado(categoria_id, modelo, genero, ano_colecao, material_id,
                                    cor, marca_id, tamanho):
    produto_verificado = Produto.query.filter(and_(Produto.categoria_id.has(categoria_id),
                                                    Produto.modelo.has(modelo),
                                                    Produto.genero.has(genero),
                                                    Produto.ano_colecao.has(ano_colecao),
                                                    Produto.material_id.has(material_id),
                                                    Produto.cor.has(cor),
                                                    Produto.marca_id.has(marca_id),
                                                    Produto.tamanho_id(tamanho))).all()
    if produto_verificado:
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

