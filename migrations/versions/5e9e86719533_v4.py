"""v4

Revision ID: 5e9e86719533
Revises: eaeb1bd07958
Create Date: 2021-07-15 04:34:29.370175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e9e86719533'
down_revision = 'eaeb1bd07958'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('table',
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('explain', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.add_column('board', sa.Column('table_name', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('board', 'table_name')
    op.drop_table('table')
    # ### end Alembic commands ###
