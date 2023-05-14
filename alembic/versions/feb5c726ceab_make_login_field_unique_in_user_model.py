"""make login field unique in user model

Revision ID: feb5c726ceab
Revises: e772b7c5b1f6
Create Date: 2023-05-14 17:28:36.094004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'feb5c726ceab'
down_revision = 'e772b7c5b1f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_login', table_name='user')
    op.create_index(op.f('ix_user_login'), 'user', ['login'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_login'), table_name='user')
    op.create_index('ix_user_login', 'user', ['login'], unique=False)
    # ### end Alembic commands ###