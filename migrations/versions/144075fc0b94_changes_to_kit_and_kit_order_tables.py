"""changes to kit and kit_order tables

Revision ID: 144075fc0b94
Revises: 2e8771443387
Create Date: 2021-11-16 16:59:49.990009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '144075fc0b94'
down_revision = '2e8771443387'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('kit_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'FK_kit_item_kit_order', 'kit_order', ['order_id'], ['id'])

    # with op.batch_alter_table('kit_order', schema=None) as batch_op:
    #    batch_op.drop_constraint(None, type_='foreignkey')
    #    batch_op.drop_column('order_item')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('kit_order', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('order_item', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(None, 'kit_item', ['order_item'], ['id'])

    with op.batch_alter_table('kit_item', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('order_id')

    # ### end Alembic commands ###
