from ..extensions import db

class Pagamentos(db.Model):
    __tablename__ = 'pagamentos'

    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    nome_completo = db.Column(db.String(100), nullable=False)

    cidade = db.Column(db.String(50), nullable=False)

    endereco = db.Column(db.String(200), nullable=False)

    numero_cartao = db.Column(db.String(16), nullable=False) # Não foi colocado o unique=True pensando que podem haver mais de um usuário com o mesmo cartão (exemplo: pai e filho tem o mesmo cartao)
    vencimento_cartao = db.Column(db.String(5), nullable=False) # formato xx/xx mês/ano
    cvv = db.Column(db.String(3), nullable=False)

    # Adicionar mais informações do cartao