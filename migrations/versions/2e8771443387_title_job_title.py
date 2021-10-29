"""title - Job title

Revision ID: 2e8771443387
Revises: 6e7e6b3304f1
Create Date: 2021-10-29 11:54:53.675066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e8771443387'
down_revision = '6e7e6b3304f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.alter_column('con_title',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.String(length=64),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.alter_column('con_title',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=8),
               existing_nullable=True)

    # ### end Alembic commands ###
