"""Create Posts table

Revision ID: 7e13def4dc73
Revises: 
Create Date: 2021-12-24 12:33:43.507556

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text



# revision identifiers, used by Alembic.
revision = '7e13def4dc73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")),
        sa.Column('owner_id', sa.Integer(), nullable=False))
#	op.create_foreign_key('posts_users_fk', source_table="Posts", referent_table="Users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
#    op.drop_constraint("posts_users_fk", tablename="Posts")
    op.drop_table("Posts")
    pass
