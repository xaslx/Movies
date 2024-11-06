from src.repositories.sql_alchemy import SQLAlchemyRepository
from src.models.favorite import Favorite
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from logger import logger



class FavoriteRepository(SQLAlchemyRepository):

    model: Favorite = Favorite


    @classmethod
    async def find_movie(cls, user_id: int, filmId: int, session: AsyncSession):
        try:
            stmt = select(cls.model).where(and_(cls.model.user_id==user_id, cls.model.film_id==filmId))
            res = await session.execute(stmt)
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f'Ошибка при поиске значения {e}')
            raise e
