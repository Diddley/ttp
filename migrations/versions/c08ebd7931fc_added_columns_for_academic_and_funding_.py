"""added columns for academic and funding to cohort

Revision ID: c08ebd7931fc
Revises: aaec4fa784b1
Create Date: 2022-05-30 15:13:12.874229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c08ebd7931fc'
down_revision = 'aaec4fa784b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('academic',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('aca_desc', sa.String(length=20), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    with op.batch_alter_table('academic', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_academic_aca_desc'), [
                              'aca_desc'], unique=False)

    op.create_table('cohort_funding',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('cf_desc', sa.String(length=20), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    with op.batch_alter_table('cohort_funding', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_cohort_funding_cf_desc'), [
                              'cf_desc'], unique=False)

    with op.batch_alter_table('cohort', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('coh_academic', sa.Integer(), nullable=True))
        batch_op.add_column(
            sa.Column('coh_fundsource', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('FK_cohort_fundSource', 'cohort_funding', [
                                    'coh_fundsource'], ['id'])
        batch_op.create_foreign_key('FK_cohort_academic', 'academic', [
                                    'coh_academic'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cohort', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('coh_fundsource')
        batch_op.drop_column('coh_academic')

    with op.batch_alter_table('cohort_funding', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_cohort_funding_cf_desc'))

    op.drop_table('cohort_funding')
    with op.batch_alter_table('academic', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_academic_aca_desc'))

    op.drop_table('academic')
    # ### end Alembic commands ###
