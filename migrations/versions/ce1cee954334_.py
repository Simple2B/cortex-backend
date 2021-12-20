"""empty message

Revision ID: ce1cee954334
Revises: 747f2180d382
Create Date: 2021-12-16 10:58:10.755449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce1cee954334'
down_revision = '747f2180d382'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('billings', sa.Column('customer_stripe_id', sa.String(length=128), nullable=True))
    op.add_column('billings', sa.Column('subscription_id', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('billings', 'subscription_id')
    op.drop_column('billings', 'customer_stripe_id')
    # ### end Alembic commands ###
