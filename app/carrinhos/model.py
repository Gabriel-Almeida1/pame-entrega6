from ..extensions import db
from ..association import association_table
from flask import jsonify

class Carrinhos(db.Model):
    __tablename__ = 'carrinhos'
    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True) # One (usuario) to One (carrinho)

    produtos = db.relationship('Produtos', secondary=association_table, backref='carrinho') # Many(carrinho) to Many(produtos)

    def json(self):
        return jsonify([produto.json() for produto in self.produtos])

    