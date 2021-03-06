"""Initial migration.

Revision ID: 57156c331c3e
Revises: 
Create Date: 2020-06-19 07:12:10.334882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57156c331c3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('geners')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('geners',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='geners_pkey')
    )
    # ### end Alembic commands ###
