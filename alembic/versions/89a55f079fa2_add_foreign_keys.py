"""add foreign keys

Revision ID: 89a55f079fa2
Revises: 29b69275740e
Create Date: 2021-12-25 19:43:01.272846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89a55f079fa2'
down_revision = '29b69275740e'
branch_labels = None
depends_on = None


def upgrade():
	op.create_foreign_key('posts_users_fk', source_table="Posts", referent_table="Users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
	pass


def downgrade():
	op.drop_constraint("posts_users_fk", tablename="Posts") 
	pass
