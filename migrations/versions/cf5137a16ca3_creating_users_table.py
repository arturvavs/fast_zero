"""creating users table

Revision ID: cf5137a16ca3
Revises: d319e62f98ac
Create Date: 2024-11-20 13:44:59.057413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf5137a16ca3'
down_revision: Union[str, None] = 'd319e62f98ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'updated_at',
               existing_type=sa.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'updated_at',
               existing_type=sa.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###
