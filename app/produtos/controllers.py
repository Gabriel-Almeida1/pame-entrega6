from flask import request, jsonify
from flask.views import MethodView
from ..extensions import db

from .model import Produtos

class ListaProdutos(MethodView): # /produtos/
    def get(self): # Ver uma lista com os produtos existentes, com seus estoques e preços
        produtos = Produtos.query.all() # Pega todos os produtos do db
        return jsonify([produto.json() for produto in produtos]), 200


class RegistrarProduto(MethodView): # /produtos/registrar

    # A ideia é que está função fosse ser utilizada somente pelo administrador da página, então ela deveria ter algum
    # tipo de autenticação por token com o id desse administrador, mas como isso atrapalharia muito na hora de testar, não coloquei.

    def post(self): # Vai ser passado "nome", "estoque" e "preco" do produto
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

class DeletarProduto(MethodView): # /produtos/excluir

    # Assim como registrar, a ideia é que está função fosse ser utilizada somente pelo administrador da página,
    # mas pelo mesmo motivo não foi colocado.

    def delete(self): # recebe "nome"
        dados = request.json

        nome_produto = dados.get('nome')

        if nome_produto == '' or nome_produto == None or not isinstance(nome_produto,str):
            return{"Erro":"Nome inválido (deve ser tipo string)"}, 400

        produto = Produtos.query.filter_by(nome=nome_produto).first()

        if not produto:
            return{"Erro":"Produto não cadastrado ou já excluído."}, 400

        db.session.delete(produto)
        db.session.commit()

        return {"mensagem":"Produto excluído do sistema."}, 200


class EstoqueProduto(MethodView): # /produtos/estoque
    def get(self): # Vai receber "nome" do produto
        dados = request.json

        nome = dados.get('nome')

        if nome == '' or nome == None or not isinstance(nome,str):
            return{"Erro":"Nome é obrigatório e deve ser tipo string"}, 400

        produto = Produtos.query.filter_by(nome=nome).first()

        if not produto:
            return{"Erro":"Produto não cadastrado"}, 400
        
        return jsonify(produto.estoque), 200

 
class PrecoProduto(MethodView): # /produtos/preco
    def get(self): # Vai receber "nome" do produto
        dados = request.json

        nome = dados.get('nome')

        if nome == '' or nome == None or not isinstance(nome,str):
            return{"Erro":"Nome é obrigatório e deve ser tipo string"}, 400

        produto = Produtos.query.filter_by(nome=nome).first()

        if not produto:
            return{"Erro":"Produto não cadastrado"}, 400
        
        return jsonify(produto.preco), 200

class SearchBar(MethodView): # /procurar

    def post(self): # recebe "procura"
        dados = request.json

        procura = dados.get('procura')

        if procura == '' or procura == None or not isinstance(procura, str):
            return{"Erro":"Input Inválido"}, 400

        aux = procura
        itens = []
        for count in range(1,len(procura)+1,1):
            item = Produtos.query.filter_by(nome=aux[0:count]).first() # Como só é permitido cadastrar 1 nome pra cada produto, nunca haverá mais de um produto achado na busca.
            if item:
                itens.append(item.json())

        if not itens:
            return {"Resultado":"Nada encontrado"}, 200

        return jsonify(itens), 200