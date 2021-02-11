from flask import request
from flask.views import MethodView
from ..extensions import db

from .model import Mensagens
from ..usuarios.model import Usuarios

class ReceberMensagem(MethodView): # /contato
    def post(self): # Recebe "text" , "email" e "assunto"
        # Vai receber um texo na "variavel" text e o email do usuario
        dados = request.json

        mensagem = dados.get('text')
        email = dados.get('email')
        assunto = dados.get('assunto')

        if mensagem == '' or mensagem == None or not isinstance(mensagem, str):
            return{"Erro":"Mensagem vazia"}, 400

        if email == '' or email == None or not isinstance(email, str):
            return{"Erro":"e-mail obrigatório"}, 400
            
        user = Usuarios.query.filter_by(email=email).first()
        if user:
            if Mensagens.query.filter_by(texto=mensagem, usuario_id=user.id).first(): # impedir flood
                return{"Erro":"Mensagem já enviada"}, 400
            mensagem = Mensagens(texto=mensagem, assunto=assunto, email=email, owner=user)
        else:
            if Mensagens.query.filter_by(texto=mensagem, email=email).first():
                return{"Erro":"Mensagem já enviada"}, 400
            mensagem = Mensagens(texto=mensagem, assunto=assunto, email=email)

        db.session.add(mensagem)
        db.session.commit()

        return mensagem.json(), 200