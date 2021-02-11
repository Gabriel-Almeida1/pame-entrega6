from flask import request, Blueprint, jsonify
from ..extensions import db
from .model import Produtos

produtos_api = Blueprint('produtos_api', __name__)

@produtos_api.route('/produtos', methods=['GET']) # Ver uma lista com os produtos existentes, com seus estoques e preços
def listaProdutos():
    produtos = Produtos.query.all() # Pega todos os produtos do db
    return jsonify([produto.json() for produto in produtos]), 200

@produtos_api.route('/produtos/registrar', methods=['POST']) # Registrar um produto novo no site
def registrarProduto():
    # Vai ser passado o nome, estoque e preco do produto
    dados = request.json

    nome = dados.get('nome')
    estoque = dados.get('estoque')
    preco = dados.get('preco')

    if nome == '' or nome == None or not isinstance(nome,str):
        return{"Erro":"Nome é obrigatório e deve ser tipo string"}, 400

    if not isinstance(estoque, int) or estoque == None:
        return{"Erro":"Estoque Inválido, deve ser tipo int"}, 400
    
    if not isinstance(preco, float) or preco == None:
        return{"Erro":"Preço Inválido, deve ser tipo float"}, 400

    if Produtos.query.filter_by(nome=nome).first():
        return{"Erro":"Produto já cadastrado"}, 400

    produto = Produtos(nome=nome, preco=preco, estoque=estoque)

    db.session.add(produto)
    db.session.commit()

    return produto.json(), 200

@produtos_api.route('/produtos/estoque', methods=['GET']) # Verificar o estoque de um produto especifico
def estoqueProduto():
    # Vai receber o nome do produto
    dados = request.json

    nome = dados.get('nome')

    if nome == '' or nome == None or not isinstance(nome,str):
        return{"Erro":"Nome é obrigatório e deve ser tipo string"}, 400

    produto = Produtos.query.filter_by(nome=nome).first()

    if not produto:
        return{"Erro":"Produto não cadastrado"}, 400
    
    return jsonify(produto.estoque), 200

@produtos_api.route('/produtos/preco', methods=['GET']) # Ver o preço de um produto específico
def precoProduto():
    # Vai receber o nome do produto
    dados = request.json

    nome = dados.get('nome')

    if nome == '' or nome == None or not isinstance(nome,str):
        return{"Erro":"Nome é obrigatório e deve ser tipo string"}, 400

    produto = Produtos.query.filter_by(nome=nome).first()

    if not produto:
        return{"Erro":"Produto não cadastrado"}, 400
    
    return jsonify(produto.preco), 200
