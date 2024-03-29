"""empty message

Revision ID: d95a7e5d9328
Revises: 
Create Date: 2020-08-18 17:23:26.512171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd95a7e5d9328'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cat_shortcode', sa.String(length=3), nullable=True),
    sa.Column('cat_desc', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_category_cat_desc'), ['cat_desc'], unique=True)
        batch_op.create_index(batch_op.f('ix_category_cat_shortcode'), ['cat_shortcode'], unique=True)

    op.create_table('division',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('div_desc', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('division', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_division_div_desc'), ['div_desc'], unique=True)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('profile', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('club',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('clb_name', sa.String(length=40), nullable=True),
    sa.Column('clb_town', sa.String(length=40), nullable=True),
    sa.Column('clb_postcode', sa.String(length=10), nullable=True),
    sa.Column('division_id', sa.Integer(), nullable=True),
    sa.Column('clb_badge', sa.String(length=40), nullable=True),
    sa.Column('clb_contract', sa.Boolean(), nullable=True),
    sa.Column('clb_collab', sa.Boolean(), nullable=True),
    sa.Column('clb_fundingapp', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['division_id'], ['division.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('club', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_club_clb_name'), ['clb_name'], unique=True)
        batch_op.create_index(batch_op.f('ix_club_clb_postcode'), ['clb_postcode'], unique=False)
        batch_op.create_index(batch_op.f('ix_club_clb_town'), ['clb_town'], unique=False)

    op.create_table('prison',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prs_name', sa.String(length=120), nullable=True),
    sa.Column('prs_town', sa.String(length=40), nullable=True),
    sa.Column('prs_category', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prs_category'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('prison', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_prison_prs_name'), ['prs_name'], unique=True)
        batch_op.create_index(batch_op.f('ix_prison_prs_town'), ['prs_town'], unique=False)

    op.create_table('cohort',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('coh_desc', sa.String(length=40), nullable=True),
    sa.Column('coh_clubid', sa.Integer(), nullable=True),
    sa.Column('coh_prisonid', sa.Integer(), nullable=True),
    sa.Column('coh_startDate', sa.DateTime(), nullable=True),
    sa.Column('coh_endDate', sa.DateTime(), nullable=True),
    sa.Column('coh_deliveryDate', sa.DateTime(), nullable=True),
    sa.Column('coh_tpi', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['coh_clubid'], ['club.id'], ),
    sa.ForeignKeyConstraint(['coh_prisonid'], ['prison.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('con_firstname', sa.String(length=64), nullable=True),
    sa.Column('con_surname', sa.String(length=64), nullable=True),
    sa.Column('con_email', sa.String(length=120), nullable=True),
    sa.Column('con_phone', sa.String(length=11), nullable=True),
    sa.Column('con_club', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['con_club'], ['club.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_contact_con_email'), ['con_email'], unique=True)
        batch_op.create_index(batch_op.f('ix_contact_con_phone'), ['con_phone'], unique=False)
        batch_op.create_index(batch_op.f('ix_contact_con_surname'), ['con_surname'], unique=False)

    op.create_table('media',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('med_clubid', sa.Integer(), nullable=True),
    sa.Column('med_prisonid', sa.Integer(), nullable=True),
    sa.Column('med_date', sa.DateTime(), nullable=True),
    sa.Column('med_medium', sa.String(length=40), nullable=True),
    sa.Column('med_publication', sa.String(length=40), nullable=True),
    sa.Column('med_link', sa.String(length=120), nullable=True),
    sa.Column('med_author', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['med_clubid'], ['club.id'], ),
    sa.ForeignKeyConstraint(['med_prisonid'], ['prison.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('funding',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fnd_cohort', sa.Integer(), nullable=True),
    sa.Column('fnd_date', sa.DateTime(), nullable=True),
    sa.Column('fnd_amount', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['fnd_cohort'], ['cohort.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('funding', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_funding_fnd_date'), ['fnd_date'], unique=False)

    op.create_table('kit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kit_cohortid', sa.Integer(), nullable=True),
    sa.Column('kit_numSmall', sa.Integer(), nullable=True),
    sa.Column('kit_numMedium', sa.Integer(), nullable=True),
    sa.Column('kit_numLarge', sa.Integer(), nullable=True),
    sa.Column('kit_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['kit_cohortid'], ['cohort.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('kit', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_kit_kit_date'), ['kit_date'], unique=False)

    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cohort_id', sa.Integer(), nullable=True),
    sa.Column('fnd_id', sa.Integer(), nullable=True),
    sa.Column('med_id', sa.Integer(), nullable=True),
    sa.Column('club_id', sa.Integer(), nullable=True),
    sa.Column('prs_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['club_id'], ['club.id'], ),
    sa.ForeignKeyConstraint(['cohort_id'], ['cohort.id'], ),
    sa.ForeignKeyConstraint(['fnd_id'], ['funding.id'], ),
    sa.ForeignKeyConstraint(['med_id'], ['media.id'], ),
    sa.ForeignKeyConstraint(['prs_id'], ['prison.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_comment_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_comment_timestamp'))

    op.drop_table('comment')
    with op.batch_alter_table('kit', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_kit_kit_date'))

    op.drop_table('kit')
    with op.batch_alter_table('funding', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_funding_fnd_date'))

    op.drop_table('funding')
    op.drop_table('media')
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_contact_con_surname'))
        batch_op.drop_index(batch_op.f('ix_contact_con_phone'))
        batch_op.drop_index(batch_op.f('ix_contact_con_email'))

    op.drop_table('contact')
    op.drop_table('cohort')
    with op.batch_alter_table('prison', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_prison_prs_town'))
        batch_op.drop_index(batch_op.f('ix_prison_prs_name'))

    op.drop_table('prison')
    with op.batch_alter_table('club', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_club_clb_town'))
        batch_op.drop_index(batch_op.f('ix_club_clb_postcode'))
        batch_op.drop_index(batch_op.f('ix_club_clb_name'))

    op.drop_table('club')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('division', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_division_div_desc'))

    op.drop_table('division')
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_category_cat_shortcode'))
        batch_op.drop_index(batch_op.f('ix_category_cat_desc'))

    op.drop_table('category')
    # ### end Alembic commands ###
