from flask import request, render_template
from flask.views import MethodView
from flask_mail import Message
from flask_jwt_extended  import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from ..extensions import db, mail

from .model import Usuarios
from ..pagamentos.model import Pagamentos

class RegistrarUsuario(MethodView): # /registrar

    def post(self): # recebe "nome", "senha", "cpf" e "data_nasc"
        dados = request.json

        nome = dados.get('nome')
        data_nasc = dados.get('data_nasc')
        cpf = dados.get('cpf')
        email = dados.get('email')
        senha = dados.get('senha')

        if nome == '' or nome == None or not isinstance(nome,str):
            return{"Erro":"Nome é obrigatório e deve ser tipo string"}, 400
        
        if email == '' or email == None or not isinstance(email,str):
            return{"Erro":"Email é obrigatório e deve ser tipo string"}, 400

        if senha == '' or senha == None or not isinstance(senha,str):
            return{"Erro":"Senha obrigatório e deve ser tipo string"}, 400

        if data_nasc == '' or data_nasc == None or not isinstance(data_nasc,str):
            return{"Erro":"Erro na Data de Nascimento (Deve ser tipo string)"}, 400

        if cpf == '' or cpf == None or not isinstance(cpf,str):
            return{"Erro":"CPF obrigatório (formato: xxx.xxx.xxx-xx) e deve ser tipo string"}, 400

        if Usuarios.query.filter_by(cpf=cpf).first():
            return{"Erro": "CPF já cadastrado"},400
        
        if Usuarios.query.filter_by(email=email).first():
            return{"Erro": "e-mail já cadastrado"},400

        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

        usuario = Usuarios(nome=nome, data_nasc=data_nasc, cpf=cpf, senha_hash=senha_hash, email=email)
        db.session.add(usuario)
        db.session.commit()

        msg = Message(sender="gabriel.avila@poli.ufrj.br",
                      recipients=[email],
                      subject='Bem vindo!',
                      html=render_template('registrar.html', nome=nome))
        mail.send(msg)
        
        return usuario.json(), 200


class UsuarioLogin(MethodView): # /login

    def post(self): # recebe "email" e "senha"
        dados = request.json

        email = dados.get('email')
        senha = dados.get('senha')

        if email == '' or email == None or not isinstance(email,str):
            return{"Erro":"Email é obrigatório e deve ser tipo string"}, 400

        if senha == '' or senha == None or not isinstance(senha,str):
            return{"Erro":"Senha obrigatória e deve ser tipo string"}, 400

        usuario = Usuarios.query.filter_by(email=email).first() # .first_or_404()
        if not usuario:
            return{"Erro": "e-mail não cadastrado"},400

        if not bcrypt.checkpw(senha.encode(), usuario.senha_hash):
            return{"Erro":"Senha Incorreta"}, 400

        token = create_access_token(identity=usuario.id)

        return {"token": token}, 200


class UsuarioCartao(MethodView): # /cartao , precisa de token

    def post(self): # Adicionar Cartao: Recebe "nome", "senha", "numero_cartao" e "cvv"
        dados = request.json

        nome = dados.get('nome')
        senha = dados.get('senha')
        numero_cartao = dados.get('numero_cartao')
        cvv = dados.get('cvv')

        if nome == '' or nome == None or not isinstance(nome,str):
            return{"Erro":"Nome é obrigatório e deve ser tipo string"}, 400

        if senha == '' or senha == None or not isinstance(senha,str):
            return{"Erro":"Senha obrigatória e deve ser tipo string"}, 400

        if numero_cartao == '' or numero_cartao == None or not isinstance(numero_cartao,str):
            return{"Erro":"Cartão é obrigatório e deve ser tipo string"}, 400

        if cvv == '' or cvv == None or not isinstance(cvv,str):
            return{"Erro":"Cvv obrigatório e deve ser tipo string"}, 400

        usuario = Usuarios.query.filter_by(nome=nome,senha=senha).first()
        if not usuario:
            return{"Erro": "Usuário não cadastrado ou usuário/senha incorreto(a)"},400
        
        if Pagamentos.query.filter_by(numero_cartao=numero_cartao, owner_id=usuario.id).first():
            return{"Erro":"Cartão já cadastrado"},400

        cartao = Pagamentos(numero_cartao=numero_cartao, cvv=cvv, owner=usuario)
        db.session.add(cartao)
        db.session.commit()

        return usuario.json(), 200     

# Adicionar funcionalidade para atualizar dados do cartao


class DadosUsuario(MethodView): # /atualizar-dados/<int:id> , precisa de token

    decorators = [jwt_required] # token, conferir se o usuario esta logado

    def put(self, id): # recebe "nome", "senha_atual", "senha_nova", "cpf", "email" e "data_nasc"
        if get_jwt_identity() != id:
            return{"Erro":"Usuário não autorizado"}, 400
        user = Usuarios.query.get_or_404(id)
        dados = request.json

        nome = dados.get('nome')
        cpf = dados.get('cpf')
        email = dados.get('email')
        data_nasc = dados.get('data_nasc')
        senha_atual = dados.get('senha_atual')
        senha_nova = dados.get('senha_nova')

        if nome == '' or nome == None or not isinstance(nome, str):
            return{"Erro":"Nome Inválido"}, 400

        if email == '' or email == None or not isinstance(email, str):
            return{"Erro":"e-mail Inválido"}, 400

        if email != user.email and Usuarios.query.filter_by(email=email).first():
            return{"Erro":"e-mail já cadastrado em outra conta"}, 400

        if senha_atual == '' or senha_atual == None or not isinstance(senha_atual, str) or not bcrypt.checkpw(senha_atual.encode(), user.senha_hash):
            return{"Erro":"Senha atual Inválida"}, 400

        if senha_nova == '' or senha_nova == None or not isinstance(senha_nova, str):
            return{"Erro":"Nova senha Inválida"}, 400

        if cpf == '' or cpf == None or not isinstance(cpf, str):
            return{"Erro":"CPF Inválido (formato: xxx.xxx.xxx-xx)"}, 400

        if Usuarios.query.filter_by(cpf=cpf).first() and Usuarios.query.filter_by(cpf=cpf).first() != user:
            return{"Erro":"CPF já cadastrado"}, 400

        if data_nasc == '' or data_nasc == None or not isinstance(data_nasc, str):
            return{"Erro":"Data de Nascimento Inválida"}, 400

        user.nome = nome 
        user.cpf = cpf
        user.email = email
        user.data_nasc = data_nasc
        user.senha_hash = bcrypt.hashpw(senha_nova.encode(), bcrypt.gensalt())

        db.session.commit()

        return user.json(), 200

    def patch(self, id):
        if get_jwt_identity() != id:
            return{"Erro":"Usuário não autorizado"}, 400
        user = Usuarios.query.get_or_404(id)
        dados = request.json

        nome = dados.get('nome', user.nome)
        cpf = dados.get('cpf', user.cpf)
        data_nasc = dados.get('data_nasc', user.data_nasc)
        senha_atual = dados.get('senha_atual', user.senha_hash)
        email = dados.get('email', user.email)
        senha_nova = dados.get('senha_nova', False)

        if nome == '' or not isinstance(nome, str):
            return{"Erro":"Nome Inválido"}, 400

        if email == '' or not isinstance(email, str):
            return{"Erro":"e-mail Inválido"}, 400

        if email != user.email and Usuarios.query.filter_by(email=email).first():
            return{"Erro":"e-mail já cadastrado em outra conta"}, 400

        if senha_atual == '' or (not isinstance(senha_atual, str) and senha_atual != user.senha_hash): 
            return{"Erro":"Senha atual Inválida"}, 400

        if senha_atual != user.senha_hash:
            if senha_nova == False:
                return{"Erro":"É preciso passar a nova senha para alterar sua senha atual"}, 400
            if not bcrypt.checkpw(senha_atual.encode(), user.senha_hash):
                return{"Erro":"Senha atual incorreta"}, 400
        
        if senha_nova == '' or (not isinstance(senha_nova, str) and senha_nova != False):
            return{"Erro":"Nova senha Inválida"}, 400

        if senha_nova != False and senha_atual == user.senha_hash:
            return{"Erro":"É preciso passar a senha atual para modificá-la"}, 400

        if cpf == '' or not isinstance(cpf, str):
            return{"Erro":"CPF Inválido (formato: xxx.xxx.xxx-xx)"}, 400

        if cpf != user.cpf and Usuarios.query.filter_by(cpf=cpf).first():
            return{"Erro":"CPF já cadastrado em outra conta"}, 400

        if data_nasc == '' or not isinstance(data_nasc, str):
            return{"Erro":"Data de Nascimento Inválida"}, 400

        user.nome = nome
        user.cpf = cpf
        user.data_nasc = data_nasc
        user.email = email
        
        if senha_atual != user.senha_hash:
            user.senha_hash = bcrypt.hashpw(senha_nova.encode(), bcrypt.gensalt())
        db.session.commit()

        return user.json(), 200

# Fazer Esqueci senha