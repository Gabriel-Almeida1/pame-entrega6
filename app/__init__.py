from flask import Flask

from .config import Config
from .extensions import db, migrate, mail, jwt

from .usuarios.model import Usuarios
from .pagamentos.model import Pagamentos
from .carrinhos.model import Carrinhos
from .produtos.model import Produtos
from .mensagens.model import Mensagens
from .itens_carrinho.model import ItensCarrinho

from .usuarios.routes import usuario_api
from .produtos.routes import produtos_api
from .carrinhos.routes import carrinhos_api
from .mensagens.routes import mensagens_api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(usuario_api)
    app.register_blueprint(produtos_api)
    app.register_blueprint(carrinhos_api)
    app.register_blueprint(mensagens_api)

    return app