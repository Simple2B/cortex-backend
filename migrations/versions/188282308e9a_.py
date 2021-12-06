"""empty message

Revision ID: 188282308e9a
Revises: 7518669397ab
Create Date: 2021-12-06 11:24:15.126514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '188282308e9a'
down_revision = '7518669397ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('billings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_billings_id'), 'billings', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_billings_id'), table_name='billings')
    op.drop_table('billings')
    # ### end Alembic commands ###
