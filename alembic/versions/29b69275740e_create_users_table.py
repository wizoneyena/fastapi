"""Create Users table

Revision ID: 29b69275740e
Revises: 7e13def4dc73
Create Date: 2021-12-24 12:47:40.781807

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = '29b69275740e'
down_revision = '7e13def4dc73'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone = True), server_default= text('now()'), nullable=False),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone = True), nullable=True),
        sa.Column('deleted', sa.Boolean(), nullable=False, default=False),\
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"))
    pass


def downgrade():
    op.drop_table("users")
    pass
