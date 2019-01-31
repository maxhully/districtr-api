"""empty message

Revision ID: 5b3b103966a4
Revises: e0d291dce089
Create Date: 2019-01-31 12:05:16.071006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b3b103966a4'
down_revision = 'e0d291dce089'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('organization', sa.String(length=160), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'organization')
    # ### end Alembic commands ###
