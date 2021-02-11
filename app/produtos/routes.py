from flask import Blueprint
from .controllers import (ListaProdutos, DeletarProduto, RegistrarProduto, EstoqueProduto, PrecoProduto)

produtos_api = Blueprint('produtos_api', __name__)

# Lista de Produtos
produtos_api.add_url_rule(
'/produtos/',
view_func=ListaProdutos.as_view('lista_produtos'),
methods=['GET']
)

# Registrar Produtos
produtos_api.add_url_rule(
'/produtos/registrar',
view_func=RegistrarProduto.as_view('registrar_produtos'),
methods=['POST']
)

# Excluir Produtos
produtos_api.add_url_rule(
'/produtos/excluir',
view_func=DeletarProduto.as_view('deletar_produtos'),
methods=['DELETE']
)

# Verificar Estoque
produtos_api.add_url_rule(
'/produtos/estoque',
view_func=EstoqueProduto.as_view('estoque_produto'),
methods=['GET']
)

# Ver Preço
produtos_api.add_url_rule(
'/produtos/preco',
view_func=PrecoProduto.as_view('preco_produto'),
methods=['GET']
)