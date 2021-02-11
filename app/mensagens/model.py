from ..extensions import db

class Mensagens(db.Model):
    __tablename__ = "mensagens"
    id = db.Column(db.Integer, primary_key=True)

    texto = db.Column(db.Text, nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def json(self):
        return{
            "mensagem": self.texto,
            "usuario_id": self.usuario_id
        }