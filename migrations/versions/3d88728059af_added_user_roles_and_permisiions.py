"""added user roles and permisiions

Revision ID: 3d88728059af
Revises: f41204e3340f
Create Date: 2021-08-31 11:53:59.044765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d88728059af'
down_revision = 'f41204e3340f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_role_default'), ['default'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_role_default'))

    op.drop_table('role')
    # ### end Alembic commands ###