"""qq

Revision ID: 9d35b30d050e
Revises: 
Create Date: 2022-12-04 23:11:26.394838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d35b30d050e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('url_map', 'short',
               existing_type=sa.VARCHAR(length=16),
               nullable=True)
    op.create_index(op.f('ix_url_map_short'), 'url_map', ['short'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_url_map_short'), table_name='url_map')
    op.alter_column('url_map', 'short',
               existing_type=sa.VARCHAR(length=16),
               nullable=False)
    # ### end Alembic commands ###