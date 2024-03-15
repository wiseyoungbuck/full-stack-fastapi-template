"""Add phones

Revision ID: 62b3e1b49207
Revises: 3b6d9e24c1d4
Create Date: 2024-03-14 22:50:55.534329

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '62b3e1b49207'
down_revision = '3b6d9e24c1d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('phone_user_id_fkey', 'phone', type_='foreignkey')
    op.drop_column('phone', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('phone', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('phone_user_id_fkey', 'phone', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
