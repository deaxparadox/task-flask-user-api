"""validation model integer id to string id

Revision ID: dc0eeec87bef
Revises: a4dc620215e3
Create Date: 2025-02-07 16:31:22.494626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'dc0eeec87bef'
down_revision: Union[str, None] = 'a4dc620215e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('validation', 'id',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=36),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('validation', 'id',
               existing_type=sa.String(length=36),
               type_=mysql.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###
