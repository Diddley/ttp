"""first migration

Revision ID: 32b1e6fc064f
Revises: 
Create Date: 2020-05-12 18:31:42.955050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32b1e6fc064f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('division',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('div_desc', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_division_div_desc'), 'division', ['div_desc'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('profile', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('club',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('town', sa.String(length=40), nullable=True),
    sa.Column('division_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['division_id'], ['division.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_club_name'), 'club', ['name'], unique=True)
    op.create_index(op.f('ix_club_town'), 'club', ['town'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_club_town'), table_name='club')
    op.drop_index(op.f('ix_club_name'), table_name='club')
    op.drop_table('club')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_division_div_desc'), table_name='division')
    op.drop_table('division')
    # ### end Alembic commands ###
