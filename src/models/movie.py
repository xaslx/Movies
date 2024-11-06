from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from sqlalchemy import JSON
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.favorite import Favorite



class Movie(Base):
    __tablename__ = 'movies'


    id: Mapped[int] = mapped_column(primary_key=True)
    filmId: Mapped[int] = mapped_column(unique=True)
    nameRu: Mapped[str | None] = mapped_column(nullable=True)
    type: Mapped[str | None] = mapped_column(nullable=True)
    year: Mapped[str | None] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    filmLength: Mapped[str | None] = mapped_column(nullable=True)
    countries: Mapped[list[str | None]] = mapped_column(JSON)
    genres: Mapped[list[str | None]] = mapped_column(JSON)
    rating: Mapped[str | None] = mapped_column(nullable=True)

    favorites: Mapped[list['Favorite']] = relationship('Favorite', back_populates='movie', cascade='all, delete-orphan')