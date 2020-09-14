"""empty message

Revision ID: b3fe1c74d97b
Revises: d724dedbe3cd
Create Date: 2020-08-20 16:57:43.500637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3fe1c74d97b'
down_revision = 'd724dedbe3cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_type', sa.String(length=12), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_course_course_type'), ['course_type'], unique=False)

    with op.batch_alter_table('cohort', schema=None) as batch_op:
        batch_op.add_column(sa.Column('coh_course', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('coh_grads', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('coh_participants', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('FK_cohort_course', 'course', ['coh_course'], ['id'])
        batch_op.drop_column('coh_deliveryDate')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cohort', schema=None) as batch_op:
        batch_op.add_column(sa.Column('coh_deliveryDate', sa.DATETIME(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('coh_participants')
        batch_op.drop_column('coh_grads')
        batch_op.drop_column('coh_course')

    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_course_course_type'))

    op.drop_table('course')
    # ### end Alembic commands ###