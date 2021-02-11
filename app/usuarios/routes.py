from flask import Blueprint
from .controllers import (RegistrarUsuario, UsuarioLogin, UsuarioPagamento, DadosUsuario, EsqueciSenha, SearchBar)

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

# Pagamento
usuario_api.add_url_rule(
'/pagamento/<int:id>', 
view_func=UsuarioPagamento.as_view('pagamento_usuario'),
methods=['POST','DELETE']
)

# Atualizar dados
usuario_api.add_url_rule(
'/atualizar-dados/<int:id>', 
view_func=DadosUsuario.as_view('atualizar_dados'),
methods=['PUT','PATCH']
)

# Esqueci minha Senha
usuario_api.add_url_rule(
'/esqueci-a-senha', 
view_func=EsqueciSenha.as_view('esqueci_senha'),
methods=['POST']
)

# Barra de pesquuisa
usuario_api.add_url_rule(
'/procurar', 
view_func=SearchBar.as_view('search_bar'),
methods=['POST']
)