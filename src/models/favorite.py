from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from src.models.user import User
    from src.models.movie import Movie


class Favorite(Base):
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    movie_id: Mapped[int] = mapped_column(ForeignKey('movies.id', ondelete='CASCADE'))
    film_id: Mapped[int]

    user: Mapped['User'] = relationship('User', back_populates='favorites')
    movie: Mapped['Movie'] = relationship('Movie', back_populates='favorites')