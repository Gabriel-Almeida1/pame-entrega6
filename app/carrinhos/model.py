from ..extensions import db
from flask import jsonify
from ..itens_carrinho.model import ItensCarrinho

class Carrinhos(db.Model):
    __tablename__ = 'carrinhos'
    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True) # One (usuario) to One (carrinho)

    itens = db.relationship('ItensCarrinho', backref='carrinho')
    
    def json(self):
        return jsonify([item.json() for item in self.itens])
