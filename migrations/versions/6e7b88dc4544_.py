"""empty message

Revision ID: 6e7b88dc4544
Revises: 2b6165814a4b
Create Date: 2016-07-11 13:28:04.669053

"""

# revision identifiers, used by Alembic.
revision = '6e7b88dc4544'
down_revision = '2b6165814a4b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('organisation_number', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer', 'organisation_number')
    ### end Alembic commands ###
