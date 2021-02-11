from .extensions import db

association_table = db.Table('association', db.Model.metadata, 
                             db.Column('carrinhos', db.Integer, db.ForeignKey('carrinhos.id')),
                             db.Column('produtos', db.Integer, db.ForeignKey('produtos.id')))