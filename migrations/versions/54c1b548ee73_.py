"""empty message

Revision ID: 54c1b548ee73
Revises: b6f5ce3efbef
Create Date: 2021-12-17 12:40:04.559801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54c1b548ee73'
down_revision = 'b6f5ce3efbef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('billings', sa.Column('payment_method', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('billings', 'payment_method')
    # ### end Alembic commands ###
