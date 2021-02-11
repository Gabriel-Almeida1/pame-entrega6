from flask import request, Blueprint
from ..extensions import db
from .model import Mensagens
from ..usuarios.model import Usuarios

mensagens_api = Blueprint('mensagens_api', __name__)

@mensagens_api.route('/fale-conosco',methods=['POST'])
def receberMensagem(): #recebe "text" e "cpf"
    # Vai receber um texo na "variavel" text e o cpf do usuario
    dados = request.json

    mensagem = dados.get('text')
    cpf = dados.get('cpf')

    if mensagem == '' or mensagem == None or not isinstance(mensagem, str):
        return{"Erro":"Mensagem vazia"}, 400

    if cpf == '' or cpf == None or not isinstance(cpf, str):
        return{"Erro":"CPF obrigatório (formato: xxx.xxx.xxx-xx)"}, 400
        
    user = Usuarios.query.filter_by(cpf=cpf).first()
    if not user:
        return{"Erro": "Usuário não cadastrado"}, 400

    if Mensagens.query.filter_by(texto=mensagem, usuario_id=user.id).first(): # impedir flood
        return{"Erro":"Mensagem já enviada"}, 400

    mensagem = Mensagens(texto=mensagem, owner=user)

    db.session.add(mensagem)
    db.session.commit()

    return mensagem.json(), 200