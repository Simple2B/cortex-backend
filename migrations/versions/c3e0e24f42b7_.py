"""empty message

Revision ID: c3e0e24f42b7
Revises: c2c6dc34c851
Create Date: 2021-11-24 14:22:58.317975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3e0e24f42b7'
down_revision = 'c2c6dc34c851'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('info_care_plans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('care_plan', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_info_care_plans_id'), 'info_care_plans', ['id'], unique=False)
    op.create_table('info_frequencies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('frequency', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_info_frequencies_id'), 'info_frequencies', ['id'], unique=False)
    op.add_column('tests', sa.Column('care_plan', sa.String(length=128), nullable=True))
    op.add_column('tests', sa.Column('frequency', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tests', 'frequency')
    op.drop_column('tests', 'care_plan')
    op.drop_index(op.f('ix_info_frequencies_id'), table_name='info_frequencies')
    op.drop_table('info_frequencies')
    op.drop_index(op.f('ix_info_care_plans_id'), table_name='info_care_plans')
    op.drop_table('info_care_plans')
    # ### end Alembic commands ###