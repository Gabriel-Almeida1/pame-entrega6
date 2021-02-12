from flask import Blueprint
from .controllers import UsuarioCarrinho

carrinhos_api = Blueprint('carrinhos_api', __name__)

# POST: adicionar item no carrinho
# GET: ver itens do carrinho
# DELETE: excluir item do carrinho

carrinhos_api.add_url_rule(
'/carrinho/<int:id>',
view_func=UsuarioCarrinho.as_view('carrinho_usuario'),
methods=['POST','GET','DELETE']
)