from flask import Blueprint
from .controllers import ReceberMensagem 

mensagens_api = Blueprint('mensagens_api', __name__)

# Receber Mensagem
mensagens_api.add_url_rule(
'/contato',
view_func=ReceberMensagem.as_view('receber_mensagem'),
methods=['POST']
)