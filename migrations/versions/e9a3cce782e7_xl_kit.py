"""XL kit

Revision ID: e9a3cce782e7
Revises: 4311b305a068
Create Date: 2020-09-11 14:30:19.434965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9a3cce782e7'
down_revision = '4311b305a068'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('kit', schema=None) as batch_op:
        batch_op.add_column(sa.Column('kit_numXlarge', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('kit', schema=None) as batch_op:
        batch_op.drop_column('kit_numXlarge')

    # ### end Alembic commands ###