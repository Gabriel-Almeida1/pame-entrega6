from flask import Flask

from .config import Config
from .extensions import db, migrate

from .usuarios.model import Usuarios
from .pagamentos.model import Pagamentos
from .carrinhos.model import Carrinhos
from .produtos.model import Produtos
from .mensagens.model import Mensagens

from .usuarios.controllers import usuario_api
from .produtos.controllers import produtos_api
from .carrinhos.controllers import carrinhos_api
from .mensagens.controllers import mensagens_api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)

    app.register_blueprint(usuario_api)
    app.register_blueprint(produtos_api)
    app.register_blueprint(carrinhos_api)
    app.register_blueprint(mensagens_api)

    return app