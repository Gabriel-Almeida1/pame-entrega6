from flask import Blueprint
from .controllers import (RegistrarUsuario, UsuarioLogin, UsuarioCartao, DadosUsuario)

usuario_api = Blueprint('usuario_api', __name__)

# Registrar
usuario_api.add_url_rule(
'/registrar', 
view_func=RegistrarUsuario.as_view('registrar_usuario'),
methods=['POST']
)

# Login
usuario_api.add_url_rule(
'/login', 
view_func=UsuarioLogin.as_view('login_usuario'),
methods=['POST']
)

# Cartao
usuario_api.add_url_rule(
'/cartao', 
view_func=UsuarioCartao.as_view('cartao_usuario'),
methods=['POST']
)

# Atualizar dados
usuario_api.add_url_rule(
'/atualizar-dados/<int:id>', 
view_func=DadosUsuario.as_view('atualizar_dados'),
methods=['PUT','PATCH']
)