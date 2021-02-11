from flask import request, Blueprint, jsonify
from ..extensions import db
from .model import Carrinhos
from ..produtos.model import Produtos
from ..usuarios.model import Usuarios

carrinhos_api = Blueprint('carrinhos_api', __name__)

@carrinhos_api.route('/carrinho/<int:id>', methods=['POST','GET'])
def index(id):
    user = Usuarios.query.get_or_404(id)
    dados = request.json

    if request.method == 'POST': # recebe "produto"
        # Vai receber o produto a ser adicionado
        nome_produto = dados.get('produto')
        
        if nome_produto == '' or nome_produto == None or not isinstance(nome_produto, str):
            return{"Erro":"Nome do produto é obrigatório e deve ser String"}, 400
        
        produto = Produtos.query.filter_by(nome=nome_produto).first()
        if not produto:
            return{"Erro": "Produto não cadastrado"}, 400

        if user.carrinho:
            carrinho = user.carrinho
            carrinho.produtos.append(produto)
            db.session.commit()
        else:
            carrinho = Carrinhos(usuario=user)
            carrinho.produtos.append(produto)
            db.session.add(carrinho)
            db.session.commit()

        return carrinho.json(), 200

    if request.method == 'GET':
        if not user.carrinho:
            return{"Erro":"Carrinho Vazio"}, 400

        return jsonify([produto.json() for produto in user.carrinho.produtos])

#    if request.method == 'DELETE':
        # Vai esvaziar o carrinho.
 #       if not user.carrinho:
  #          return{"Erro":"Carrinho já está Vazio"}, 400
        
   #     for produto in user.carrinho.produtos:
    #        print(produto)
     #       db.session.delete(produto)
      #      db.session.commit()

       # return user.json(), 200