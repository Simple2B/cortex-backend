"""empty message

Revision ID: 468a144c66d6
Revises:
Create Date: 2021-10-01 15:54:16.919512

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "468a144c66d6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "conditions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_conditions_id"), "conditions", ["id"], unique=False)
    op.create_table(
        "diseases",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_diseases_id"), "diseases", ["id"], unique=False)
    op.create_table(
        "client_conditions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=True),
        sa.Column("condition_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["clients.id"],
        ),
        sa.ForeignKeyConstraint(
            ["condition_id"],
            ["conditions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_client_conditions_id"), "client_conditions", ["id"], unique=False
    )
    op.create_table(
        "client_diseases",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=True),
        sa.Column("disease_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["clients.id"],
        ),
        sa.ForeignKeyConstraint(
            ["disease_id"],
            ["diseases.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_client_diseases_id"), "client_diseases", ["id"], unique=False
    )
    op.add_column("clients", sa.Column("birthday", sa.Date(), nullable=True))
    op.add_column("clients", sa.Column("phone", sa.String(length=32), nullable=True))
    op.add_column(
        "clients", sa.Column("medications", sa.String(length=128), nullable=True)
    )
    op.add_column(
        "clients", sa.Column("covid_tested_positive", sa.Boolean(), nullable=True)
    )
    op.add_column("clients", sa.Column("covid_vaccine", sa.Boolean(), nullable=True))
    op.add_column("clients", sa.Column("stressful_level", sa.Integer(), nullable=True))
    op.add_column(
        "clients", sa.Column("consent_minor_child", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "clients", sa.Column("relationship_child", sa.String(), nullable=True)
    )
    op.add_column("clients", sa.Column("api_key", sa.String(length=36), nullable=True))
    op.alter_column(
        "clients", "first_name", existing_type=sa.VARCHAR(length=64), nullable=False
    )
    op.alter_column(
        "clients", "last_name", existing_type=sa.VARCHAR(length=64), nullable=False
    )
    op.drop_index("ix_clients_phone_num", table_name="clients")
    op.create_index(op.f("ix_clients_phone"), "clients", ["phone"], unique=True)
    op.drop_column("clients", "date_of_birthday")
    op.drop_column("clients", "phone_num")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "clients",
        sa.Column(
            "phone_num", sa.VARCHAR(length=32), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "clients",
        sa.Column(
            "date_of_birthday",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_index(op.f("ix_clients_phone"), table_name="clients")
    op.create_index("ix_clients_phone_num", "clients", ["phone_num"], unique=False)
    op.alter_column(
        "clients", "last_name", existing_type=sa.VARCHAR(length=64), nullable=True
    )
    op.alter_column(
        "clients", "first_name", existing_type=sa.VARCHAR(length=64), nullable=True
    )
    op.drop_column("clients", "api_key")
    op.drop_column("clients", "relationship_child")
    op.drop_column("clients", "consent_minor_child")
    op.drop_column("clients", "stressful_level")
    op.drop_column("clients", "covid_vaccine")
    op.drop_column("clients", "covid_tested_positive")
    op.drop_column("clients", "medications")
    op.drop_column("clients", "phone")
    op.drop_column("clients", "birthday")
    op.drop_index(op.f("ix_client_diseases_id"), table_name="client_diseases")
    op.drop_table("client_diseases")
    op.drop_index(op.f("ix_client_conditions_id"), table_name="client_conditions")
    op.drop_table("client_conditions")
    op.drop_index(op.f("ix_diseases_id"), table_name="diseases")
    op.drop_table("diseases")
    op.drop_index(op.f("ix_conditions_id"), table_name="conditions")
    op.drop_table("conditions")
    # ### end Alembic commands ###
