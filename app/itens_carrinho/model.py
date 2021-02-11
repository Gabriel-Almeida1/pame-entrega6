from ..extensions import db

class ItensCarrinho(db.Model):
    __tablename__ = 'itens-carrinho'
    id = db.Column(db.Integer, primary_key=True)

    nome_produto = db.Column(db.String(20), unique=True, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    unidades = db.Column(db.Integer, nullable=False)

    carrinho_id = db.Column(db.Integer, db.ForeignKey('carrinhos.id'))

    def json(self):
        return{
            "nome": self.nome_produto,
            "unidades": self.unidades,
            "preco": self.preco
        }