from flask import request, jsonify
from flask.views import MethodView
from ..extensions import db

from .model import Carrinhos
from ..produtos.model import Produtos
from ..usuarios.model import Usuarios
from ..itens_carrinho.model import ItensCarrinho

class UsuarioCarrinho(MethodView): # /carrinho/<int:id>
    def get(self, id):
        user = Usuarios.query.get_or_404(id)
        dados = request.json
        if not user.carrinho:
            return{"Mensagem":"Carrinho Vazio"}, 200

        return jsonify([item.json() for item in user.carrinho.itens]),200

    def post(self, id): # recebe "produto"
        # Vai receber o produto a ser adicionado
        user = Usuarios.query.get_or_404(id)
        dados = request.json

        nome_produto = dados.get('produto')
        
        if nome_produto == '' or nome_produto == None or not isinstance(nome_produto, str):
            return{"Erro":"Nome do produto é obrigatório e deve ser String"}, 400
        
        produto = Produtos.query.filter_by(nome=nome_produto).first()
        if not produto:
            return{"Erro": "Produto não cadastrado"}, 400

        if user.carrinho:
            print("if")
            carrinho = user.carrinho 
            achou = False

            for count in range (0,len(carrinho.itens),1):
                if carrinho.itens[count].nome_produto == produto.nome:
                    carrinho.itens[count].unidades += 1
                    achou = True
                    break # dado que não existirão produtos repetidos nessa lista

            if achou == False:
                item = ItensCarrinho(nome_produto=nome_produto,preco=produto.preco, unidades=1, carrinho=carrinho)
                db.session.add(item)

            db.session.commit()

        else:
            print("else")
            carrinho = Carrinhos(usuario=user)
            item = ItensCarrinho(nome_produto=nome_produto,preco=produto.preco, unidades=1, carrinho=carrinho)
            db.session.add(carrinho)
            db.session.add(item)
            db.session.commit()

        return carrinho.json(), 200


'''
    if request.method == 'DELETE':
         Vai esvaziar o carrinho.
        if not user.carrinho:
            return{"Erro":"Carrinho já está Vazio"}, 400
        
        for produto in user.carrinho.produtos:
            print(produto)
            db.session.delete(produto)
            db.session.commit()

        return user.json(), 200
'''