from os import abort
from jinja2 import Template
from sqlalchemy.orm import base
from sqlalchemy.orm.base import manager_of_class
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import true
from estoque import app
from flask import render_template, redirect, url_for, flash, send_from_directory, session, request
from flask_login import login_user, logout_user, login_required, current_user
from estoque.models import Produto, User, Material, Fornecedor, Marca, Categoria, Tamanho, HistoricoPrecos, MovimentacaoProduto, Situacao
from estoque import db
from estoque.forms import AlteraSenhaForm, RegisterForm, LoginForm, FornecedorForm, ProdutoForm, MarcaForm, ConsultaForm, AtualizacaoForm, SelecionaDataForm
from estoque.gerar_pdf import *
from datetime import date, timedelta
from sqlalchemy import or_, and_ , func
import re, os
import os.path
import time, threading
from flask import abort, jsonify


def gera_nome_colunas():
    return ['Descrição','Modelo','Gênero','Coleção','Material','Cor','Preço','Qtde','Marca','Tamanho']

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

# ==============================================================================================================
# ====================================== ÁREA DAS ROTAS DOS PRODUTOS ===========================================
# ==============================================================================================================
@app.route('/estoque_mostra', methods=['GET','POST'])
@login_required
def mostrar_tela_de_estoque():
    pagina=request.args.get('pagina',1,type=int)
    resultado = Produto.query.filter(Produto.situacao_id==1).order_by(Produto.descricao.asc()).paginate(per_page=10, page=pagina, error_out=True)
    marcas=Marca.query.all()
    tamanhos=Tamanho.query.all()
    materiais=Material.query.all()
    categorias = Categoria.query.all()    
    quantidade = resultado.total
    colunas = gera_nome_colunas()
    label_categoria = gera_label_para_checkbox_categoria()
    label_ano=gera_label_para_checkbox_ano_colecao()
    label_marca = gera_label_para_checkbox_marca()
    label_material = gera_label_para_checkbox_material()
    return render_template('estoque_mostrar.html', resultado=resultado, colunas=colunas, label_categoria=label_categoria, 
                           label_ano=label_ano, label_marca=label_marca, label_material=label_material, 
                           quantidade=quantidade, marcas=marcas, tamanhos=tamanhos, 
                           materiais=materiais, categorias=categorias)

@app.route('/estoque', methods=['POST'])
@login_required
def estoque_page():
    session.modified = True
    pagina = request.args.get('pagina',1, type=int)
    atualiza_form = AtualizacaoForm()
    colunas = gera_nome_colunas()
    marcas=Marca.query.all()
    tamanhos=Tamanho.query.all()
    materiais=Material.query.all()
    categorias = Categoria.query.all()    
    label_categoria = gera_label_para_checkbox_categoria()
    label_ano=gera_label_para_checkbox_ano_colecao()
    label_marca = gera_label_para_checkbox_marca()
    label_material = gera_label_para_checkbox_material()
    consultar = request.form['consultar'].lower()
    resultado = consulta(consultar, pagina)
    quantidade=resultado.total
    return render_template('estoque_consulta.html', resultado=resultado, colunas=colunas, label_categoria=label_categoria, 
                        label_ano=label_ano, label_marca=label_marca, label_material=label_material, 
                        genero="", atualiza_form=atualiza_form, consultar=consultar, quantidade=quantidade,
                        marcas=marcas, tamanhos=tamanhos, materiais=materiais, categorias=categorias)

@app.route('/atualiza_produto', methods=['POST'])
@login_required
def atualiza_produto():
    session.modified = True
    produto = Produto.query.filter_by(id=request.form['id_produto']).first()
    produto.descricao = request.form['descricao'].lower()
    produto.ano_colecao = request.form['ano']
    produto.tamanho_id = request.form['tamanho']
    produto.categoria_id = request.form['categoria']
    produto.modelo = request.form['modelo'].lower()
    produto.genero = request.form['genero'].lower()
    produto.material_id = request.form['material']
    produto.cor = request.form['cor'].lower()
    produto.marca_id = request.form['marca']
    db.session.commit()
    flash(f'Produto {produto.id} - {produto.descricao} alterado com sucesso', category='success')
    return redirect(url_for('mostrar_tela_de_estoque', pagina=1))

@app.route('/deletar_produto')
@login_required
def deletar_produto():
    id=request.args.get('id_produto')
    produto=Produto.query.filter_by(id=id).first()
    produto.situacao_id = 2
    db.session.commit()
    flash(f'Produto ID: {produto.id}, Descrição: {produto.descricao} deletado com sucesso.', category='success')
    return redirect(url_for('mostrar_tela_de_estoque'))


@app.route('/masculino')
@login_required
def produtos_masculinos():    
    pagina = request.args.get('pagina',1, type=int)
    session.modified = True
    marcas=Marca.query.all()
    tamanhos=Tamanho.query.all()
    materiais=Material.query.all()
    categorias = Categoria.query.all()   
    atualiza_form = AtualizacaoForm()
    colunas = gera_nome_colunas()
    label_categoria = gera_label_para_checkbox_categoria()
    label_ano=gera_label_para_checkbox_ano_colecao()
    label_marca = gera_label_para_checkbox_marca()
    label_material = gera_label_para_checkbox_material()
    resultado = Produto.query.filter(and_(Produto.genero == "masculino", Produto.situacao_id == 1)).order_by(Produto.descricao.asc()).paginate(per_page=10, page=pagina, error_out=True)
    quantidade = resultado.total
    return render_template('estoque_masculino.html', resultado=resultado, colunas=colunas, label_categoria=label_categoria, quantidade=quantidade,
                           label_ano=label_ano, label_marca=label_marca, label_material=label_material, genero="masculino", atualiza_form=atualiza_form,
                           marcas=marcas, tamanhos=tamanhos, materiais=materiais, categorias=categorias)

@app.route('/feminino')
@login_required
def produtos_feminino():
    pagina = request.args.get('pagina',1, type=int)
    session.modified = True
    marcas=Marca.query.all()
    tamanhos=Tamanho.query.all()
    materiais=Material.query.all()
    categorias = Categoria.query.all() 
    atualiza_form = AtualizacaoForm()
    colunas = gera_nome_colunas()
    label_categoria = gera_label_para_checkbox_categoria()
    label_ano=gera_label_para_checkbox_ano_colecao()
    label_marca = gera_label_para_checkbox_marca()
    label_material = gera_label_para_checkbox_material()
    resultado = Produto.query.filter(and_(Produto.genero == "feminino", Produto.situacao_id == 1)).order_by(Produto.descricao.asc()).paginate(per_page=10, page=pagina, error_out=True)
    quantidade = resultado.total
    return render_template('estoque_feminino.html', resultado=resultado, colunas=colunas, label_categoria=label_categoria, quantidade=quantidade,
                           label_ano=label_ano, label_marca=label_marca, label_material=label_material, genero="feminino", atualiza_form=atualiza_form,
                           marcas=marcas, tamanhos=tamanhos, materiais=materiais, categorias=categorias)

def consulta(atributo_para_consulta, pagina):
    condicao = Produto.query.filter(or_(Produto.categoria.has(Categoria.descricao.contains(atributo_para_consulta)),
                                        Produto.tamanho_id.contains(atributo_para_consulta),
                                        Produto.marca.has(Marca.nome.contains(atributo_para_consulta)), 
                                        Produto.ano_colecao.contains(atributo_para_consulta),
                                        Produto.material.has(Material.descricao.contains(atributo_para_consulta)),
                                        Produto.descricao.contains(atributo_para_consulta),
                                        Produto.modelo.contains(atributo_para_consulta))/and_(Produto.situacao_id==1)).order_by(Produto.descricao.asc()).paginate(per_page=10, page=pagina, error_out=True)
    if condicao :
        return condicao
    return False

@app.route('/estoque_checkbox', methods=['POST'])
@login_required
def busca_valores_checkbox():
    session.modified = True
    marcas=Marca.query.all()
    tamanhos=Tamanho.query.all()
    materiais=Material.query.all()
    categorias = Categoria.query.all() 
    pagina= request.args.get('pagina', 1, type=int)
    atualiza_form = AtualizacaoForm()
    colunas = gera_nome_colunas()
    label_categoria = gera_label_para_checkbox_categoria()
    label_ano=gera_label_para_checkbox_ano_colecao()
    label_marca = gera_label_para_checkbox_marca()
    label_material = gera_label_para_checkbox_material()
    resultado=''
    genero=''
    lista_tamanhos = request.form.getlist('tamanho')
    lista_categoria = request.form.getlist('categoria')
    lista_ano_colecao = request.form.getlist('ano')
    lista_marca = request.form.getlist('marca')
    lista_material = request.form.getlist('material')
    genero = request.form['genero']
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
    resultado = filtrar_check_box( pagina, genero, lista_tamanhos, lista_categoria, 
                                lista_ano_colecao, lista_marca, lista_material)
    quantidade = resultado.total  
    return render_template('consulta_checkbox.html', resultado=resultado, colunas=colunas, label_categoria=label_categoria, 
                                            label_ano=label_ano, label_marca=label_marca, label_material=label_material, 
                                            genero=genero, atualiza_form=atualiza_form, lista_tamanhos=lista_tamanhos,
                                            lista_categoria=lista_categoria, lista_ano_colecao=lista_ano_colecao,
                                            lista_marca=lista_marca, lista_material=lista_material, quantidade=quantidade,
                                            marcas=marcas, tamanhos=tamanhos, materiais=materiais, categorias=categorias)

@app.route('/mostra_resultado_checkbox', methods=["GET"])
def mostra_resultado_checkbox():
    session.modified = True
    marcas=Marca.query.all()
    tamanhos=Tamanho.query.all()
    materiais=Material.query.all()
    categorias = Categoria.query.all()    
    pagina= request.args.get('pagina', 1, type=int)
    atualiza_form = AtualizacaoForm()
    colunas = gera_nome_colunas()
    label_categoria = gera_label_para_checkbox_categoria()
    label_ano=gera_label_para_checkbox_ano_colecao()
    label_marca = gera_label_para_checkbox_marca()
    label_material = gera_label_para_checkbox_material()
    lista_tamanhos = request.args.getlist('lista_tamanhos')
    lista_categoria = request.args.getlist('lista_categoria')
    lista_ano_colecao = request.args.getlist('lista_ano_colecao')
    lista_marca = request.args.getlist('lista_marca')
    lista_material = request.args.getlist('lista_material')
    genero = request.args.get('genero')
    resultado = filtrar_check_box( pagina, genero, lista_tamanhos, lista_categoria, lista_ano_colecao, lista_marca, lista_material)
    quantidade = resultado.total   
    return render_template('consulta_checkbox.html', resultado=resultado, colunas=colunas, label_categoria=label_categoria, 
                                            label_ano=label_ano, label_marca=label_marca, label_material=label_material, 
                                            genero=genero, atualiza_form=atualiza_form, lista_tamanhos=lista_tamanhos,
                                            lista_categoria=lista_categoria, lista_ano_colecao=lista_ano_colecao,
                                            lista_marca=lista_marca, lista_material=lista_material, quantidade=quantidade,
                                            marcas=marcas, tamanhos=tamanhos, materiais=materiais, categorias=categorias)

def filtrar_check_box(pagina, genero, lista_tamanhos, 
                        lista_categoria, lista_ano_colecao, lista_marca, lista_material):
    resultado = ''
    if genero != '':
        resultado = Produto.query.filter(and_(Produto.genero == genero,
                                        Produto.categoria_id.in_(lista_categoria),
                                        Produto.tamanho_id.in_(lista_tamanhos),
                                        Produto.material_id.in_(lista_material),
                                        Produto.marca_id.in_(lista_marca),
                                        Produto.ano_colecao.in_(lista_ano_colecao))).order_by(Produto.descricao.asc()).paginate(per_page=10, page=pagina, error_out=True)
    else:
        resultado = Produto.query.filter(and_(Produto.tamanho_id.in_(lista_tamanhos),
                                        Produto.categoria_id.in_(lista_categoria),
                                        Produto.material_id.in_(lista_material),
                                        Produto.marca_id.in_(lista_marca),
                                        Produto.ano_colecao.in_(lista_ano_colecao))).order_by(Produto.descricao.asc()).paginate(per_page=10, page=pagina, error_out=True) 
    return resultado

@app.route('/cadastrar_produto', methods=['GET'])
@login_required
def mostrar_tela_de_cadastro_do_produto():
    form = ProdutoForm()
    categorias = [(categoria.id, categoria.descricao.title()) for categoria in Categoria.query.order_by(Categoria.descricao.asc()).all()]
    form.categoria.choices = categorias
    form.marca.choices = [(marca.id, marca.nome.title()) for marca in Marca.query.order_by(Marca.nome.asc()).all()]
    form.material.choices = [(material.id, material.descricao.title()) for material in Material.query.order_by(Material.descricao.asc()).all()]
    return render_template('cadastrar_produto.html', form=form, categorias=categorias)

@app.route('/cadastrar_produto', methods=['POST'])
@login_required
def cadastrar_produto():
    try:
        session.modified = True    
        form = ProdutoForm()
        categorias = [(categoria.id, categoria.descricao.title()) for categoria in Categoria.query.order_by(Categoria.descricao).all()]
        form.categoria.choices = categorias
        form.marca.choices = [(marca.id, marca.nome.title()) for marca in Marca.query.order_by(Marca.nome).all()]
        form.material.choices = [(material.id, material.descricao.title()) for material in Material.query.order_by(Material.descricao).all()]
        validar_quantidade = validar_quantidade_informada(request.form['quantidade'])
        validar_produto = verificar_se_produto_cadastrado(request.form['categoria'],request.form['modelo'].lower(), 
                                                            request.form['genero'].lower(), request.form['ano_colecao'],
                                                            request.form['material'], request.form['cor'].lower(), 
                                                            request.form['marca'], request.form['tamanho'].lower())
        validar_preco = validar_preco_informado(request.form['preco'])
        if validar_preco != False and validar_preco != None:
            if validar_quantidade != False and validar_quantidade != None:
                if validar_produto == False:
                    if int(request.form['ano_colecao']) >= 2019 and int(request.form['ano_colecao']) <= 2022:                
                        produto_criado = Produto(categoria_id = request.form['categoria'],
                                            descricao = request.form['descricao'].lower(),
                                            modelo = request.form['modelo'].lower(), 
                                            ano_colecao = request.form['ano_colecao'],
                                            material_id = request.form['material'],
                                            genero = request.form['genero'].lower(),
                                            cor = form.cor.data.lower(),
                                            preco = validar_preco,
                                            quantidade = validar_quantidade,
                                            tamanho_id = request.form['tamanho'].lower(),
                                            marca_id = request.form['marca'],
                                            situacao_id = 1)
                        db.session.add(produto_criado)
                        db.session.commit()
                        registra_historico_de_preco = HistoricoPrecos(id_produto = produto_criado.id,
                                                                preco = validar_preco,
                                                                quantidade = validar_quantidade)
                        registra_movimentacao = MovimentacaoProduto(user_id = current_user.id,
                                                                    produto_id = produto_criado.id,
                                                                    quantidade = produto_criado.quantidade,
                                                                    valor = (-1)*(produto_criado.quantidade * produto_criado.preco),
                                                                    tipo_movimentacao = 'entrada')   
                        db.session.add(registra_movimentacao)
                        db.session.add(registra_historico_de_preco)
                        db.session.commit() 
                        flash(f'Produto {produto_criado.categoria.descricao} cadastrado com sucesso', category='success')
                    else:
                        flash("Ano da coleção deve ser maior que 2019 e menor que 2023.", category='danger')
                else:
                    flash("Produto já cadastrado.", category='danger')                
            else:
                flash("Quantidade inválida! Informe apenas números inteiros maior que 0.", category='danger') 
        else:
            flash("Preço inválido! Informe apenas números positivos e separados por . ou ,", category='danger')
        return render_template('cadastrar_produto.html', form=form, categorias=categorias)
    except:
        flash("Não foi possível o cadastramento do produto, verifique todos os campos e tente novamente.", category='danger')
        return render_template('cadastrar_produto.html', form=form, categorias=categorias)


# ==============================================================================================================
# =================================FIM DA ÁREA DAS ROTAS DOS PRODUTOS ==========================================
# ==============================================================================================================

@app.route('/alteracao_preco', methods=['POST'])
@login_required
def alteracao_preco_produto():
    id_produto = request.form['produto']
    preco = validar_preco_informado(request.form['preco'])
    produto = Produto.query.filter_by(id=id_produto).first()
    if preco:
        registra_movimentacao = MovimentacaoProduto(user_id = current_user.id,
                                                            produto_id = id_produto,
                                                            quantidade = produto.quantidade,
                                                            valor = (preco * produto.quantidade) - (produto.preco * produto.quantidade),
                                                            tipo_movimentacao = 'alteração preço')
        registra_historico_de_preco = HistoricoPrecos(id_produto = id_produto,
                                                        preco = preco,
                                                        quantidade = produto.quantidade)
        produto.preco = preco
        db.session.add(registra_historico_de_preco)
        db.session.add(registra_movimentacao)
        db.session.commit()
        flash('Preço alterado com sucesso', category='success')
        return redirect(url_for('mostrar_tela_de_estoque'))
    flash('Não foi possível atualizar o preço. Tente novamente', category='success')
    return redirect(url_for('mostrar_tela_de_estoque'))

@app.route('/registra_entrada_produto', methods=['POST'])
@login_required
def entrada_produto():
    try:
        session.modified = True
        id_produto = int(request.form['produto'])
        produto = Produto.query.filter_by(id=id_produto).first()
        quantidade_da_entrada = validar_quantidade_informada(request.form['quantidade'])
        preco_do_produto = validar_preco_informado(request.form['preco'])
        total_estoque = quantidade_da_entrada + produto.quantidade
        if total_estoque <= 20:
            if preco_do_produto and quantidade_da_entrada:
                if preco_do_produto != produto.preco:
                    registra_movimentacao = MovimentacaoProduto(user_id = current_user.id,
                                                                produto_id = id_produto,
                                                                quantidade = quantidade_da_entrada,
                                                                valor = (quantidade_da_entrada * preco_do_produto)*(-1),
                                                                tipo_movimentacao = 'entrada')
                    registra_historico_de_preco = HistoricoPrecos(id_produto = id_produto,
                                                                preco = produto.preco,
                                                                quantidade = quantidade_da_entrada)
                    if produto.quantidade > 0:
                        registra_movimentacao2 = MovimentacaoProduto(user_id = current_user.id,
                                                                    produto_id = id_produto,
                                                                    quantidade = produto.quantidade,
                                                                    valor = (produto.quantidade * preco_do_produto)
                                                                            - (quantidade_da_entrada * produto.preco),
                                                                    tipo_movimentacao = 'impacto estoque atual')
                        db.session.add(registra_movimentacao2)
                    produto.preco = preco_do_produto
                else:
                    registra_movimentacao = MovimentacaoProduto(user_id = current_user.id,
                                                                produto_id = id_produto,
                                                                quantidade = quantidade_da_entrada,
                                                                valor = (quantidade_da_entrada * produto.preco)*(-1),
                                                                tipo_movimentacao = 'entrada')
                    registra_historico_de_preco = HistoricoPrecos(id_produto = id_produto,
                                                                preco = produto.preco,
                                                                quantidade = quantidade_da_entrada)
                soma_da_entrada = produto.quantidade + quantidade_da_entrada
                produto.quantidade = soma_da_entrada
                db.session.add(registra_historico_de_preco)
                db.session.add(registra_movimentacao)
                db.session.commit()
                flash('Entrada do produto realizada com sucesso!', category="success")
        else:
            flash('A quantidade de produtos em estoque não deve passar de 20.', category='warning')
        
        return redirect(url_for('mostrar_tela_de_estoque'))

    except:
        flash('Não foi possível realizar a entrada, tente novamente!', category="danger")
        return redirect(url_for('mostrar_tela_de_estoque'))

@app.route('/registra_saida_produto', methods=['POST'])
@login_required
def saida_produto():
    try:
        session.modified = True
        id_produto = int(request.form['produto'])
        produto = Produto.query.filter_by(id=id_produto).first()
        quantidade_da_saida = validar_quantidade_informada(request.form['quantidade'])
        preco_do_produto = validar_preco_informado(request.form['preco'])    
        validar_saida = produto.quantidade - quantidade_da_saida
        if quantidade_da_saida <= produto.quantidade:
            if preco_do_produto != produto.preco:
                registra_movimentacao = MovimentacaoProduto(user_id = current_user.id,
                                            produto_id = id_produto,
                                            quantidade = quantidade_da_saida,
                                            valor = preco_do_produto * quantidade_da_saida,
                                            tipo_movimentacao = 'saída preço alterado')
                registra_historico_de_preco = HistoricoPrecos(id_produto = id_produto,
                                                            preco = produto.preco,
                                                            quantidade = quantidade_da_saida)
            else:
                registra_movimentacao = MovimentacaoProduto(user_id = current_user.id,
                                                        produto_id = id_produto,
                                                        quantidade = quantidade_da_saida,
                                                        valor = preco_do_produto * quantidade_da_saida,
                                                        tipo_movimentacao = 'saída')
                registra_historico_de_preco = HistoricoPrecos(id_produto = id_produto,
                                                            preco = produto.preco,
                                                            quantidade = quantidade_da_saida)
            produto.quantidade = validar_saida
            db.session.add(registra_movimentacao)
            db.session.add(registra_historico_de_preco)
            db.session.commit()
            flash('Saída realizada com sucesso!', category="success")
            return redirect(url_for('mostrar_tela_de_estoque'))
        else:
            flash('Quantidade de saída maior que a disponível!', category='danger')
        return redirect(url_for('mostrar_tela_de_estoque'))
    except:
        flash('Não foi possível efetuar a saída. Tente novamente.', category='danger')
        return redirect(url_for('mostrar_tela_de_estoque'))


# ===========================================================================================================


@app.route('/mostrar_relatorio', methods=['GET'])
@login_required
def mostra_tela_relatorio_movimentacao():
    gera_nome_colunas_movimentacao = ['Produto','Marca', 'Usuário', 'Dia', 'Quantidade', 'Valor', 'Tipo da Movimentação']
    pagina=request.args.get('pagina',1,type=int)
    produto=Produto.query.all()
    ultimos_trinta_dias = (date.today()) - timedelta(days=30)
    form = SelecionaDataForm(data_inicial=ultimos_trinta_dias, data_final=date.today())
    data_inicial = form.data_inicial.data
    data_final = form.data_final.data
    lista_categoria = request.form.getlist('categoria')
    lista_marca = request.form.getlist('marca')
    lista_movimentacao = request.form.getlist('movimento')
    label_categoria = gera_label_para_checkbox_categoria()
    label_marca = gera_label_para_checkbox_marca()
    nome_do_arquivo = 'vazio'   
    produtos_movimentados = filtar_produtos_movimentados(pagina,lista_categoria, data_inicial, data_final,
                                                        lista_marca, lista_movimentacao)
    quantidade = produtos_movimentados.total
    return render_template('relatorio_movimentacao.html', label_categoria=label_categoria, label_marca=label_marca, 
                                                        produto=produto, form=form, colunas=gera_nome_colunas_movimentacao,
                                                        compras=0, vendas=0, ajuste=0,impacto=0, mais_vendido=[['Nada',0]],menos_vendido="[['Nada',0]]", 
                                                        data_inicial_guardada = data_inicial,  data_final_guardada=data_final,
                                                        nome_do_arquivo = nome_do_arquivo, produtos_movimentados=produtos_movimentados, 
                                                        quantidade=quantidade)
                           


@app.route('/relatorio_movimentacao', methods=['POST'])
@login_required
def relatorio_movimentacao():
    pagina=request.args.get('pagina',1,type=int)
    session.modified = True
    gera_nome_colunas_movimentacao = ['Produto','Marca', 'Usuário', 'Dia', 'Qtde', 'Valor', 'Movimentação']
    form = SelecionaDataForm()
    label_categoria = gera_label_para_checkbox_categoria()
    label_marca = gera_label_para_checkbox_marca()
    data_inicial = form.data_inicial.data
    data_final = form.data_final.data
    hoje = date.today()
    lista_categoria = request.form.getlist('categoria')
    lista_marca = request.form.getlist('marca')
    lista_movimentacao = request.form.getlist('movimento')
    nome_do_arquivo = ''
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
        lista_movimentacao = ['alteração preço','entrada','impacto estoque atual','saída', 'saída preço alterado']    
    produtos_movimentados = filtar_produtos_movimentados(pagina,lista_categoria, data_inicial, data_final,
                                                        lista_marca, lista_movimentacao)
    quantidade = produtos_movimentados.total
    produtos_para_relatorio = filtar_produtos_movimentados_relatorio(lista_categoria, data_inicial, data_final,
                                                        lista_marca, lista_movimentacao)
    valor_estoque = db.session.query(func.sum(Produto.preco)).all()
    quantidade_estoque = db.session.query(func.sum(Produto.quantidade)).all()
    valor_do_estoque = (formatar_moeda(valor_estoque[0][0]*quantidade_estoque[0][0]))
    quantidade_estoque = int(quantidade_estoque[0][0])
    pdf = PDF('L','mm','A4')
    nome_do_arquivo = pdf.body(produtos_para_relatorio)
    movimentos= separar_movimentacoes(produtos_para_relatorio)
    mais_vendido = produtos_mais_vendidos()
    menos_vendido = produtos_menos_vendidos()
    chama_funcao_apagar = threading.Thread(target = apagar_arquivo, args = (nome_do_arquivo,))
    chama_funcao_apagar.start()
    return render_template('relatorio_movimentacao_consulta.html', label_categoria=label_categoria,
                            data_inicial_guardada = data_inicial, data_final_guardada = data_final,
                            lista_categoria=lista_categoria, lista_marca=lista_marca,lista_movimentacao=lista_movimentacao,
                           label_marca=label_marca, produtos_movimentados=produtos_movimentados, form=form, 
                           colunas=gera_nome_colunas_movimentacao, impacto=movimentos['impacto'],
                           compras=movimentos['compras'], vendas=movimentos['vendas'], mais_vendido=mais_vendido, menos_vendido=menos_vendido,
                           ajuste=movimentos['ajuste'], nome_do_arquivo=nome_do_arquivo, quantidade=quantidade,
                           valor_do_estoque=valor_do_estoque, quantidade_estoque=quantidade_estoque)

def segunda_posicao(lista):
    return lista[1]

def produtos_mais_vendidos():
    mais_vendidos = db.session.query(
    Produto.descricao,
    func.sum(MovimentacaoProduto.quantidade)).filter(MovimentacaoProduto.quantidade > 0).outerjoin(MovimentacaoProduto, Produto.id == MovimentacaoProduto.produto_id).\
    group_by(Produto.id).all()
    mais_vendidos.sort(key=segunda_posicao, reverse=True)
    return mais_vendidos

def produtos_menos_vendidos():
    menos_vendidos = db.session.query(
    Produto.descricao,
    func.sum(MovimentacaoProduto.quantidade)).filter(MovimentacaoProduto.quantidade > 0).outerjoin(MovimentacaoProduto, Produto.id == MovimentacaoProduto.produto_id).\
    group_by(Produto.id).all()
    menos_vendidos.sort(key=segunda_posicao)
    return menos_vendidos


def separar_movimentacoes(produtos_movimentados):
    compras = 0
    vendas = 0
    ajuste = 0
    impacto = 0
    sobras = 0
    if len(produtos_movimentados) > 0:
        for produto in produtos_movimentados:
            if produto.tipo_movimentacao == 'alteração preço':
                ajuste += produto.valor
            elif produto.tipo_movimentacao == 'entrada':
                compras += produto.valor
            elif produto.tipo_movimentacao == 'impacto estoque atual':
                impacto += produto.valor
            elif produto.tipo_movimentacao == 'saída' or produto.tipo_movimentacao == "saída preço alterado":
                vendas += produto.valor
            else:
                sobras += produto.valor
    else:
        pass
    return ({'vendas':vendas, 'compras':compras, 'ajuste':ajuste, 'impacto':impacto})


@app.route('/mostra_resultado_relatorio')
@login_required
def mostra_resultado_relatorio_financeiro():
    session.modified = True
    gera_nome_colunas_movimentacao = ['Produto','Marca', 'Usuário', 'Dia', 'Quantidade', 'Valor', 'Tipo da Movimentação']
    marcas=Marca.query.all()    
    categorias = Categoria.query.all()    
    movimentacao = MovimentacaoProduto.query.all()
    ultimos_trinta_dias = (date.today()) - timedelta(days=30)
    ultimos_trinta_dias = (date.today()) - timedelta(days=30)
    form = SelecionaDataForm(data_inicial=ultimos_trinta_dias, data_final=date.today())
    pagina=request.args.get('pagina',1,type=int)
    produto=Produto.query.all()
    lista_categoria = request.args.getlist('lista_categoria')
    lista_marca = request.args.getlist('lista_marca')
    lista_movimentacao = request.args.getlist('lista_movimentacao')
    data_inicial_guardada = request.args.get('data_inicial_guardada')
    data_final_guardada = request.args.get('data_final_guardada')
    impacto = request.args.get('impacto')
    mais_vendido = produtos_mais_vendidos()
    menos_vendido = produtos_menos_vendidos()
    compras=request.args.get('compras')
    vendas=request.args.get('vendas')
    ajuste=request.args.get('ajuste')
    label_categoria = gera_label_para_checkbox_categoria()
    label_marca = gera_label_para_checkbox_marca()
    produtos_movimentados = filtar_produtos_movimentados(pagina,lista_categoria, data_inicial_guardada, data_final_guardada,
                                                        lista_marca, lista_movimentacao)
    quantidade=produtos_movimentados.total
    valor_estoque = db.session.query(func.sum(Produto.preco)).all()
    valor_estoque = float(valor_estoque[0][0])
    quantidade_estoque = db.session.query(func.sum(Produto.quantidade)).all()
    quantidade_estoque = int(quantidade_estoque[0][0])
    valor_do_estoque = (formatar_moeda(valor_estoque*quantidade_estoque))
    return render_template('relatorio_movimentacao_consulta.html', 
                            label_categoria=label_categoria, label_marca=label_marca, marcas=marcas, categorias=categorias,
                            movimentacao=movimentacao, produto=produto, form=form, colunas=gera_nome_colunas_movimentacao,
                            compras=compras, vendas=vendas, ajuste=ajuste, quantidade=quantidade, data_inicial_guardada=data_inicial_guardada,
                            data_final_guardada=data_final_guardada, produtos_movimentados=produtos_movimentados, 
                            lista_categoria=lista_categoria, lista_marca=lista_marca, lista_movimentacao=lista_movimentacao,
                            impacto=impacto,menos_vendido=menos_vendido, mais_vendido=mais_vendido, valor_do_estoque=valor_do_estoque,
                            quantidade_estoque=quantidade_estoque)

def filtar_produtos_movimentados(pagina,lista_categoria, data_inicial, data_final,
                                        lista_marca, lista_movimentacao):
    produtos_movimentados = ""
    produtos_movimentados = MovimentacaoProduto.query.filter(and_(MovimentacaoProduto.data.between(data_inicial, data_final),
                                                        MovimentacaoProduto.produto.has(Produto.categoria_id.in_(lista_categoria)),
                                                        MovimentacaoProduto.produto.has(Produto.marca_id.in_(lista_marca)),
                                                        MovimentacaoProduto.tipo_movimentacao.in_(lista_movimentacao))).\
                                                        order_by(MovimentacaoProduto.produto.has(Produto.categoria_id).asc()).\
                                                        paginate(per_page=10, page=pagina, error_out=True)
    return produtos_movimentados

def filtar_produtos_movimentados_relatorio(lista_categoria, data_inicial, data_final,
                                        lista_marca, lista_movimentacao):
    produtos_movimentados = ""
    produtos_movimentados = MovimentacaoProduto.query.filter(and_(MovimentacaoProduto.data.between(data_inicial, data_final),
                                                        MovimentacaoProduto.produto.has(Produto.categoria_id.in_(lista_categoria)),
                                                        MovimentacaoProduto.produto.has(Produto.marca_id.in_(lista_marca)),
                                                        MovimentacaoProduto.tipo_movimentacao.in_(lista_movimentacao))).\
                                                        order_by(MovimentacaoProduto.produto.has(Produto.categoria_id).asc()).all()
    return produtos_movimentados


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/relatorio_pdf/<arquivo>')
@login_required
def gerar_pdf(arquivo):
    try:
        leitura_do_arquivo = send_from_directory(app.config['CLIENT_PDF'],
                                    arquivo,
                                    as_attachment=True)
        chama_funcao_apagar = threading.Thread(target = apagar_arquivo, args = (arquivo, ))
        chama_funcao_apagar.start()
        return leitura_do_arquivo
    except FileNotFoundError:
        return redirect(url_for('relatorio_movimentacao'))    


def apagar_arquivo(nome_do_arquivo):
    time.sleep(60)
    try:
        os.remove(f"{app.config['RAIZ']}/{app.config['CLIENT_PDF']}/{nome_do_arquivo}")
    except:
        pass

@app.template_filter()
def formatar_moeda(preco):
    preco = float(preco)
    a = f'{preco:,.2f}'
    b = a.replace(',','v')
    c = b.replace('.',',')
    preco = c.replace('v','.')
    return f'R${preco}'


@app.route('/lista_fornecedores', methods=['GET'])
@login_required
def mostra_lista_de_fornecedores():
    form = FornecedorForm()
    pagina=request.args.get('pagina', 1, type=int)
    situacoes=Situacao.query.all()
    fornecedores = Fornecedor.query.filter(Fornecedor.situacao_id == 1).order_by(Fornecedor.name.asc()).\
                    paginate(per_page=10, page=pagina, error_out=True)
    quantidade=fornecedores.total
    marcas = Marca.query.all()
    return render_template('fornecedores_lista.html', situacoes=situacoes,quantidade=quantidade,form=form, fornecedores=fornecedores, marcas=marcas)

@app.route('/lista_fornecedores_inativos', methods=['GET'])
@login_required
def mostra_lista_de_fornecedores_inativos():
    form = FornecedorForm()
    pagina=request.args.get('pagina', 1, type=int)
    situacoes=Situacao.query.all()
    fornecedores = Fornecedor.query.filter(Fornecedor.situacao_id == 2).order_by(Fornecedor.name.asc()).\
                    paginate(per_page=10, page=pagina, error_out=True)
    quantidade=fornecedores.total
    marcas = Marca.query.all()
    return render_template('fornecedores_lista_inativos.html', situacoes=situacoes,quantidade=quantidade,form=form, fornecedores=fornecedores, marcas=marcas)


@app.route('/lista_marcas_fornecedor', methods=['POST'])
@login_required
def listar_marcas_fornecedores():
    id = request.form['fornecedor_id']
    marcas = Marca.query.filter_by(fornecedor_id=id).\
                        order_by(Marca.nome.desc()).all()
    if len(marcas) == 0:
        return redirect(url_for('mostra_lista_de_fornecedores'))
    return marcas

@app.template_filter()
def formatar_telefone(telefone):
    lista = []
    for x in telefone:
        lista.append(x)
    if len(lista) == 11:
        telefone = f"({''.join(lista[:2])}){''.join(lista[2:7])}-{''.join(lista[7:])}"
    else:
        telefone = f"({''.join(lista[:2])}){''.join(lista[2:6])}-{''.join(lista[6:])}"
    return telefone

@app.template_filter()
def formatar_cnpj(cnpj):
    lista = []
    for x in cnpj:
        lista.append(x)
    print('lista inicial',len(lista))
    for x in range(1,15):
        if len(lista) < 14:
            lista.insert(0,'0')
    print('lista final',len(lista), "".join(lista))
    cnpj = f"{''.join(lista[:2])}.{''.join(lista[2:5])}.{''.join(lista[5:8])}/{''.join(lista[8:12])}-{''.join(lista[12:])}"
    return cnpj


@app.route('/cadastrar_fornecedor', methods=['POST'])
@login_required
def cadastrar_fornecedor():
    session.modified = True
    form = FornecedorForm()
    if form.validate_on_submit():
        if len(request.form['cnpj']) < 15:
            fornecedor_to_create = Fornecedor(name = form.name.data,
                                            email = form.email.data,
                                            fone = request.form['fone'],
                                            cnpj = request.form['cnpj'],
                                            situacao_id = 1)
            db.session.add(fornecedor_to_create)
            db.session.commit()
            flash(f'Fornecedor {fornecedor_to_create.name} cadastrado com sucesso', category='success')
            return redirect(url_for('mostra_lista_de_fornecedores'))
        else:
            flash(f'CNPJ com mais de 14 caracteres', category='danger')
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro ao cadastrar o fornecedor: {err_msg}', category='danger')
    return redirect(url_for('mostra_lista_de_fornecedores'))

@app.route('/atualizar_fornecedor', methods=['POST'])
@login_required
def atualizar_fornecedor():
    id=request.form['id_fornecedor']
    fornecedor= Fornecedor.query.filter_by(id=id).first()
    fornecedor.name = request.form["nome"].lower()
    fornecedor.email = request.form["email"]
    fornecedor.fone = request.form["telefone"]
    fornecedor.cnpj = request.form["cnpj"]
    fornecedor.situacao_id = request.form["situacao"]
    db.session.commit()
    flash('Fornecedor atualizado com sucesso.', category='success')
    return redirect(url_for('mostra_lista_de_fornecedores'))

@app.route('/ativar_fornecedor', methods=["POST"])
@login_required
def reativar_fornecedor():
    id=request.form['fornecedor_id']
    fornecedor=Fornecedor.query.filter_by(id=id).first()
    fornecedor.situacao_id = 1
    db.session.commit()
    flash(f'Marca ID: {fornecedor.id}, Descrição: {fornecedor.name.title()} reativada com sucesso.', category='success')
    return redirect(url_for('mostra_lista_de_fornecedores_inativos'))

@app.route('/inativar_fornecedor', methods=["POST"])
@login_required
def deletar_fornecedor():
    id=request.form['fornecedor_id']
    fornecedor=Fornecedor.query.filter_by(id=id).first()
    fornecedor.situacao_id = 2
    db.session.commit()
    flash(f'Marca ID: {fornecedor.id}, Descrição: {fornecedor.name.title()} reativada com sucesso.', category='success')
    return redirect(url_for('mostra_lista_de_fornecedores'))


@app.route('/mostrar_cadastrar_marca', methods=['GET'])
@login_required
def mostrar_tela_de_cadastramento_de_marcas():
    session.modified = True
    pagina=request.args.get('pagina', 1, type=int)
    fornecedores = Fornecedor.query.order_by(Fornecedor.name.asc()).all()
    marcas = Marca.query.filter(Marca.situacao_id==1).order_by(Marca.nome.asc()).paginate(per_page=10, page=pagina, error_out=True)
    quantidade=marcas.total
    fornecedores = Fornecedor.query.all()
    return render_template('marcas_mostrar.html', fornecedores=fornecedores,marcas=marcas, quantidade=quantidade)

@app.route('/marcas_inativa', methods=['GET'])
@login_required
def marcas_inativas():
    session.modified = True
    pagina=request.args.get('pagina', 1, type=int)
    fornecedores = Fornecedor.query.order_by(Fornecedor.name.asc()).all()
    marcas = Marca.query.filter(Marca.situacao_id==2).order_by(Marca.nome.asc()).paginate(per_page=10, page=pagina, error_out=True)
    quantidade=marcas.total
    fornecedores = Fornecedor.query.all()
    return render_template('marcas_inativas.html', fornecedores=fornecedores, marcas=marcas, quantidade=quantidade)

@app.route('/cadastrar_marca', methods=['POST'])
@login_required
def cadastrar_marca():
    session.modified = True
    valida_marca = verifica_marca_existente(request.form['marca_nome'].lower())
    if not valida_marca:
        marca_criada = Marca(nome=request.form['marca_nome'].lower(),
                            fornecedor_id = request.form['fornecedor1'],
                            fornecedor_id_2 = request.form['fornecedor2'],
                            fornecedor_id_3 = request.form['fornecedor3'],
                            situacao_id = 1)
        db.session.add(marca_criada)
        db.session.commit()
        flash(f'Marca {marca_criada.nome.title()} cadastrada com sucesso', category='success')
    else:
        flash('Marca já está cadastrada!', category="danger")
    return redirect(url_for('mostrar_tela_de_cadastramento_de_marcas'))

@app.route('/atualizar_marca', methods=['POST'])
@login_required
def atualizar_marca():
    id = request.form['marca_id']
    marca = Marca.query.filter_by(id=id).first() 
    marca.nome = request.form['marca_nome'].lower()
    marca.fornecedor_id = request.form['fornecedor1']
    marca.fornecedor_id_2 = request.form['fornecedor2']
    marca.fornecedor_id_3 = request.form['fornecedor3']
    db.session.commit()
    flash(f'Marca #ID: {id} - Nome: {marca.nome.title()} atualizada com sucesso!', category='success')
    return redirect(url_for('mostrar_tela_de_cadastramento_de_marcas'))

@app.route('/deletar_marca', methods=["POST"])
@login_required
def deletar_marca():
    id=request.form['marca_id']
    marca=Marca.query.filter_by(id=id).first()
    marca.situacao_id = 2
    db.session.commit()
    flash(f'Marca ID: {marca.id}, Descrição: {marca.nome.title()} inativada com sucesso.', category='success')
    return redirect(url_for('mostrar_tela_de_cadastramento_de_marcas'))


@app.route('/ativar_marca', methods=["POST"])
@login_required
def reativar_marca():
    id=request.form['marca_id']
    marca=Marca.query.filter_by(id=id).first()
    marca.situacao_id = 1
    db.session.commit()
    flash(f'Marca ID: {marca.id}, Descrição: {marca.nome.title()} reativada com sucesso.', category='success')
    return redirect(url_for('mostrar_tela_de_cadastramento_de_marcas'))


@app.route('/mostrar_funcionarios', methods=["GET"])
@login_required
def funcionarios_mostrar():
    form = RegisterForm()
    atualiza_funci = AlteraSenhaForm()
    cargos = Cargos.query.order_by(Cargos.descricao.asc()).all()
    situacoes= SituacaoFuncionario.query.filter(SituacaoFuncionario.id != 2).all()
    pagina=request.args.get('pagina',1, type=int)
    funcionarios = User.query.filter(User.situacao_id==1).order_by(User.name.asc()).paginate(per_page=10, page=pagina, error_out=True )
    quantidade=funcionarios.total
    return render_template('funcionarios_mostrar.html', situacoes=situacoes, atualiza_funci=atualiza_funci, cargos=cargos, form=form, funcionarios=funcionarios, pagina=pagina, quantidade=quantidade)

@app.route('/mostrar_funcionarios_afastados', methods=["GET"])
@login_required
def funcionarios_afastados_mostrar():
    form = RegisterForm()
    atualiza_funci = AlteraSenhaForm()
    situacoes= SituacaoFuncionario.query.filter(SituacaoFuncionario.id != 2).all()
    cargos = Cargos.query.order_by(Cargos.descricao.asc()).all()
    pagina=request.args.get('pagina',1, type=int)
    funcionarios = User.query.filter(User.situacao_id != 1).order_by(User.name.asc()).paginate(per_page=10, page=pagina, error_out=True )
    quantidade=funcionarios.total
    return render_template('funcionarios_afastados_mostrar.html', situacoes=situacoes,atualiza_funci=atualiza_funci, cargos=cargos, form=form, funcionarios=funcionarios, pagina=pagina, quantidade=quantidade)


@app.route('/atualizacao_funcionario', methods=["POST"])
@login_required
def funcionario_atualiza():
    try:
        id_funcionario = request.form['id_funcionario']  
        funcionario=User.query.filter_by(id=id_funcionario).first()
        funcionario.name = request.form['nome'].lower()
        funcionario.username = request.form['usuario']
        if current_user.cargo_id == 1:
            funcionario.cargo_id = request.form['cargo']
        db.session.commit()
        flash('Dados alterados com sucesso.', category='danger')
        return redirect(url_for('funcionarios_mostrar'))
    except:
        flash('Apenas funcionários autorizados podem atualizar o cargo.', category='danger')
        return redirect(url_for('funcionarios_mostrar'))

@app.route('/resetar_senha', methods=["POST"])
@login_required
def funcionario_reseta_senha():
    try:
        administrador = current_user.cargo_id
        id_funcionario = request.form['id_funcionario']
        funcionario = User.query.filter_by(id=id_funcionario).first()
        if administrador == 1:
            funcionario.password = '123456'
            db.session.commit()
            flash('Senha resetada com sucesso.', category="success")
        else:
            flash('Você não tem permissão para esta funcionalidade, entre em contato com o administrador.', category="danger")
        return redirect(url_for('funcionarios_mostrar'))
    except:
        flash('Não foi possível alterar a senha.', category="danger")
        return redirect(url_for('funcionarios_mostrar'))


@app.route('/altera_senha', methods=["POST"])
@login_required
def funcionario_altera_senha():
    atualiza_funci = AlteraSenhaForm()
    try:
        id_funcionario = request.form['id_funcionario']
        funcionario = User.query.filter_by(id=id_funcionario).first()
        if funcionario.check_password_correction(
            attempted_password=atualiza_funci.senha_atual.data):
            if atualiza_funci.nova_senha.data == atualiza_funci.nova_senha_confirmar.data:
                funcionario.password = atualiza_funci.nova_senha.data
                db.session.commit()
                flash('Senha alterada com sucesso!', category='success')
            else:
                flash('Senha nova e sua confirmação não são iguais.', category='danger')
        else:
            flash('A senha atual não confere com a anterior', category='danger')
        return redirect(url_for('funcionarios_mostrar'))
    except:
        flash('Não foi possível alterar a senha.', category='danger')
        return redirect(url_for('funcionarios_mostrar'))
        


@app.route('/cadastrar_funcionario', methods=['GET', 'POST'])
@login_required
def register_page():
    session.modified = True
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data.lower(),
                            name = form.name.data.lower(),
                            cargo_id = request.form['cargo'],
                            password = form.password.data,
                            situacao_id = 1,
                            )
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Conta criada com suecesso.', category='success')
        return redirect(url_for('funcionarios_mostrar', pagina=1))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'Não foi possível a criação do usuário: {err_msg}', category='danger')

    return redirect(url_for('funcionarios_mostrar', pagina=1))

@app.route('/afastar_funcionarios', methods=["POST"])
@login_required
def funcionarios_afastar():
    id = request.form['id_funcionario']
    funcionario=User.query.filter_by(id=id).first()
    funcionario.situacao_id = request.form['situacao']
    db.session.commit()
    flash('Situação alterada com sucesso.', category='danger')
    return redirect(url_for('funcionarios_mostrar'))


@app.route('/demitir_funcionarios', methods=["POST"])
@login_required
def funcionarios_demitir():
    try:
        administrador = current_user.cargo_id
        id_funci = request.form['id_funci']
        funcionario = User.query.filter_by(id=id_funci).first()
        if administrador == 1:
            funcionario.situacao_id = 2
            db.session.commit()
            flash(f'Funcionário {funcionario.name.title()} demitido com sucesso.', category='danger')
        else:
            flash('Você não tem permissão para esta funcionalidade, entre em contato com o administrador.', category="danger")
        return redirect(url_for('funcionarios_mostrar'))
    except:
        flash('Ocorreu um erro ao cadastrar o funcionário tente novamente', category="danger")
        return redirect(url_for('funcionarios_mostrar', pagina=1))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            if attempted_user.situacao_id == 1 or attempted_user.cargo_id == 1:
                login_user(attempted_user)
                flash(f'Sucesso! Usuário logado: {attempted_user.username}', category='success')
                session.permanent = True
                session.modified = True
                return redirect(url_for('mostrar_tela_de_estoque', pagina=1))
            flash(f'Funcionário não pode logar, motivo: {attempted_user.situacao.descricao}', category='danger')
        else:
            flash('Usuário e senha não correspondem! Tente novamente', category='danger')    
    flash("Não possui senha ou esqueceu? Solicite o acesso aos administradores.", category="warning")
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Você foi deslogado!', category='info')
    return redirect(url_for('home_page'))

# ==============================================================================================
# ================================ FUNÇÕES SEM ROTA ============================================
# ==============================================================================================
def validar_preco_informado(preco_informado):
    try:
        preco_informado = preco_informado.strip()
        preco_formatado = ''
        if 'R$' in preco_informado:
            preco_informado = preco_informado.replace('R$','')
        if re.match("^[1-9]\d{0,7}((\.|\,)\d{1,4})$",preco_informado):
            preco_formatado = preco_informado.replace(',', '.')
            return float(preco_formatado)
        elif re.match("^[1-9]",preco_informado):
            return float(preco_informado)
    except ValueError:
        return False

def validar_quantidade_informada(quantidade_informada):
	try:
		val=int(quantidade_informada)
		if (val>=0):
			return val
	except:
	    return False    

def validar_texto(texto_informado):
	if (texto_informado.replace(" ","").isalpha()):
		return True
	else:
		return False

def verifica_marca_existente(nome):
    procurar_marca = Marca.query.filter_by(nome=nome).first()
    if procurar_marca:
        return True
    return False
    
def verificar_se_produto_cadastrado(categoria_id, modelo, genero, ano_colecao, material_id,
                                    cor, marca_id, tamanho):                                                     
    produto_verificado = Produto.query.filter(and_(Produto.categoria_id == categoria_id,
                                                    Produto.modelo == modelo,
                                                    Produto.genero == genero,
                                                    Produto.ano_colecao == ano_colecao,
                                                    Produto.material_id == material_id,
                                                    Produto.cor == cor, Produto.marca_id == marca_id,
                                                    Produto.tamanho_id == tamanho)).first()
    if produto_verificado:
        return True
    return False