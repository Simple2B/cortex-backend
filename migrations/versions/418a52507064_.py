"""empty message

Revision ID: 418a52507064
Revises: c91dec0ef941
Create Date: 2021-12-22 19:01:05.946288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '418a52507064'
down_revision = 'c91dec0ef941'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('billings', sa.Column('status', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('billings', 'status')
    # ### end Alembic commands ###
