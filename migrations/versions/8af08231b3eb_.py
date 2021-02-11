"""empty message

Revision ID: 8af08231b3eb
Revises: 
Create Date: 2021-02-10 20:58:12.746816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8af08231b3eb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('produtos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=20), nullable=False),
    sa.Column('estoque', sa.Integer(), nullable=True),
    sa.Column('preco', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=30), nullable=False),
    sa.Column('data_nasc', sa.String(length=10), nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.Column('senha', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf')
    )
    op.create_table('carrinhos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('usuario_id')
    )
    op.create_table('mensagens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('texto', sa.Text(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pagamentos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('numero_cartao', sa.String(length=16), nullable=True),
    sa.Column('cvv', sa.String(length=3), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association',
    sa.Column('carrinhos', sa.Integer(), nullable=True),
    sa.Column('produtos', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['carrinhos'], ['carrinhos.id'], ),
    sa.ForeignKeyConstraint(['produtos'], ['produtos.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association')
    op.drop_table('pagamentos')
    op.drop_table('mensagens')
    op.drop_table('carrinhos')
    op.drop_table('usuarios')
    op.drop_table('produtos')
    # ### end Alembic commands ###
