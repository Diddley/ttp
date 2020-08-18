"""new fields club

Revision ID: 7a5af81eb7be
Revises: 910e847acc4e
Create Date: 2020-08-17 16:40:14.119272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a5af81eb7be'
down_revision = '910e847acc4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('club', schema=None) as batch_op:
        batch_op.add_column(sa.Column('clb_badge', sa.String(length=40), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('club', schema=None) as batch_op:
        batch_op.drop_column('clb_badge')

    # ### end Alembic commands ###
