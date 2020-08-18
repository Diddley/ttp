"""empty message

Revision ID: ebe01c87b05f
Revises: 7a5af81eb7be
Create Date: 2020-08-17 17:13:57.883806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebe01c87b05f'
down_revision = '7a5af81eb7be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('club', schema=None) as batch_op:
        batch_op.add_column(sa.Column('clb_collab', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('clb_contract', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('clb_fundingapp', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('club', schema=None) as batch_op:
        batch_op.drop_column('clb_fundingapp')
        batch_op.drop_column('clb_contract')
        batch_op.drop_column('clb_collab')

    # ### end Alembic commands ###
