from ..extensions import db
from ..association import association_table

class Produtos(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(20), nullable=False)
    estoque = db.Column(db.Integer) # número de unidades disponíveis
    preco = db.Column(db.Float) 

    carrinhos = db.relationship("Carrinhos", secondary=association_table, backref='produto') # Many(carrinho) to Many(produtos)
    
    def json(self):
        return{
            "nome": self.nome,
            "estoque": self.estoque,
            "preco": self.preco
        }