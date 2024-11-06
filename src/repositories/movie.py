from src.repositories.sql_alchemy import SQLAlchemyRepository
from src.models.movie import Movie
from sqlalchemy import select
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.favorite import Favorite
from sqlalchemy.exc import SQLAlchemyError
from logger import logger


class MovieRepository(SQLAlchemyRepository):

    model: Movie = Movie


    @classmethod
    async def get_favorite_movies(cls, user_id: int, session: AsyncSession):
        try:
            stmt = (select(cls.model)
            .join(Favorite, cls.model.id == Favorite.movie_id)
            .where(Favorite.user_id == user_id)
            .options(
                load_only(
                    cls.model.filmId, cls.model.nameRu, cls.model.year, 
                    cls.model.filmLength, cls.model.genres, cls.model.type, 
                    cls.model.description, cls.model.countries, cls.model.rating
                    )
                ))
            result = await session.execute(stmt)
            return result.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f'Не удалось найти значение: {e}')
            raise e