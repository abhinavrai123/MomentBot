"""renamed text -> column to avoid any confusion

Revision ID: 5c3da124ee29
Revises: d14b93513c23
Create Date: 2025-07-24 13:53:43.968971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c3da124ee29'
down_revision: Union[str, None] = 'd14b93513c23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
