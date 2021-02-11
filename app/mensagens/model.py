from ..extensions import db

class Mensagens(db.Model):
    __tablename__ = "mensagens"
    id = db.Column(db.Integer, primary_key=True)
    
    assunto = db.Column(db.String(150))
    texto = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100))

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    def json(self):
        return{
            "mensagem": self.texto,
            "usuario_id": self.usuario_id,
            "assunto": self.assunto,
            "email": self.email
        }