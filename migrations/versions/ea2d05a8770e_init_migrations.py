"""init migrations

Revision ID: ea2d05a8770e
Revises: 
Create Date: 2025-02-05 16:20:47.247504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea2d05a8770e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('type', sa.Enum('Employee', 'TeamLead', 'Manager', name='usertype'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'type')
    # ### end Alembic commands ###
