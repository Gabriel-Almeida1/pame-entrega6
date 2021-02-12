from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended  import jwt_required, get_jwt_identity
from ..extensions import db

from .model import Carrinhos
from ..produtos.model import Produtos
from ..usuarios.model import Usuarios
from ..itens_carrinho.model import ItensCarrinho

class UsuarioCarrinho(MethodView): # /carrinho/<int:id>

    decorators = [jwt_required]

    def get(self, id):
        if get_jwt_identity() != id:
            return{"Erro":"Usuário não autorizado"}, 400
        user = Usuarios.query.get_or_404(id)

        if not user.carrinho or not user.carrinho.itens:
            return{"Mensagem":"Carrinho Vazio"}, 200

        return jsonify([item.json() for item in user.carrinho.itens]),200

    def post(self, id): # recebe "produto"
        # Vai receber o produto a ser adicionado
        if get_jwt_identity() != id:
            return{"Erro":"Usuário não autorizado"}, 400
        user = Usuarios.query.get_or_404(id)
        dados = request.json

        nome_produto = dados.get('produto')
        
        if nome_produto == '' or nome_produto == None or not isinstance(nome_produto, str):
            return{"Erro":"Nome do produto é obrigatório e deve ser String"}, 400
        
        produto = Produtos.query.filter_by(nome=nome_produto).first()
        if not produto:
            return{"Erro": "Produto não cadastrado"}, 400

        if user.carrinho:
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

        else:
            carrinho = Carrinhos(usuario=user)
            item = ItensCarrinho(nome_produto=nome_produto,preco=produto.preco, unidades=1, carrinho=carrinho)
            db.session.add(carrinho)
            db.session.add(item)
        
        db.session.commit()

        return carrinho.json(), 200

    def delete(self, id): # recebe "produto"
        # Vai deletar 1 unidade por vez
        if get_jwt_identity() != id:
            return{"Erro":"Usuário não autorizado"}, 400
        user = Usuarios.query.get_or_404(id)
        dados = request.json

        nome_produto = dados.get('produto')

        if nome_produto == '' or nome_produto == None or not isinstance(nome_produto, str):
            return{"Erro":"Nome do produto é obrigatório e deve ser String"}, 400
        
        if not user.carrinho:
            return{"Erro":"Carrinho está vazio"}, 400
        
        achou = False
        for count in range(0,len(user.carrinho.itens),1):
            if user.carrinho.itens[count].nome_produto == nome_produto:
                item = user.carrinho.itens[count]
                achou = True
                break
        
        if achou == False:
            return{"Erro":"Produto não encontrado no carrinho"}, 400
        
        item.unidades -= 1

        if item.unidades == 0:
            db.session.delete(item)
        
        db.session.commit()

        return {"Mensagem":"Item excluído com sucesso"}, 200
        