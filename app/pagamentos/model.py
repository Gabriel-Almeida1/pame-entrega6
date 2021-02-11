from ..extensions import db

class Pagamentos(db.Model):
    __tablename__ = 'pagamentos'

    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    numero_cartao = db.Column(db.String(16)) # Não foi colocado o unique=True pensando que podem haver mais de um usuário com o mesmo cartão (exemplo: pai e filho tem o mesmo cartao)
    cvv = db.Column(db.String(3))