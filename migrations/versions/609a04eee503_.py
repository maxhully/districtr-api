"""empty message

Revision ID: 609a04eee503
Revises: 76d5771b3125
Create Date: 2019-04-03 12:30:19.818041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "609a04eee503"
down_revision = "76d5771b3125"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "unit_set",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=True),
        sa.Column("unit_type", sa.String(length=80), nullable=False),
        sa.Column("place_id", sa.Integer(), nullable=True),
        sa.Column("id_column_key", sa.String(length=80), nullable=True),
        sa.ForeignKeyConstraint(["place_id"], ["place.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "column_set",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("type", sa.String(length=80), nullable=False),
        sa.Column("unit_set_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["unit_set_id"], ["unit_set.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_constraint("column_election_id_fkey", "column", type_="foreignkey")
    op.add_column("column", sa.Column("column_set_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "column", "column_set", ["column_set_id"], ["id"])
    op.drop_column("column", "election_id")
    op.add_column("tileset", sa.Column("unit_set_id", sa.Integer(), nullable=True))
    op.drop_constraint("tileset_place_id_fkey", "tileset", type_="foreignkey")
    op.create_foreign_key(None, "tileset", "unit_set", ["unit_set_id"], ["id"])
    op.drop_column("tileset", "place_id")
    op.drop_table("election")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tileset",
        sa.Column("place_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "tileset", type_="foreignkey")
    op.create_foreign_key(
        "tileset_place_id_fkey", "tileset", "place", ["place_id"], ["id"]
    )
    op.drop_column("tileset", "unit_set_id")
    op.add_column(
        "column",
        sa.Column("election_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "column", type_="foreignkey")
    op.create_foreign_key(
        "column_election_id_fkey", "column", "election", ["election_id"], ["id"]
    )
    op.drop_column("column", "column_set_id")
    op.create_table(
        "election",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("race", sa.VARCHAR(length=80), autoincrement=False, nullable=False),
        sa.Column("year", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("place_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["place_id"], ["place.id"], name="election_place_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="election_pkey"),
    )
    op.drop_table("column_set")
    op.drop_table("unit_set")
    # ### end Alembic commands ###