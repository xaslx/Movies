"""empty message

Revision ID: 773da2c6fbdb
Revises: 9a6e5c4e3c4d
Create Date: 2024-11-06 10:29:21.369610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '773da2c6fbdb'
down_revision: Union[str, None] = '9a6e5c4e3c4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('favorites_movie_id_fkey', 'favorites', type_='foreignkey')
    op.create_foreign_key(None, 'favorites', 'movies', ['movie_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'favorites', type_='foreignkey')
    op.create_foreign_key('favorites_movie_id_fkey', 'favorites', 'movies', ['movie_id'], ['id'])
    # ### end Alembic commands ###
