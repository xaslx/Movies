from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from logger import logger
from src.repositories.base import AbstractRepository



class SQLAlchemyRepository(AbstractRepository):

    model = None

    @classmethod
    async def add(cls, session: AsyncSession, **data: dict,
    ):
        try:
            stmt = (
                insert(cls.model)
                .values(**data)
                .returning(cls.model.__table__.columns)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при добавлении записи в базу данных",
                extra={"данные": data, "ошибка": e},
            )
            raise 


    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by,
    ):
   
        try:
            stmt = select(cls.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                "Ошибка при добавлении записи в базу данных",
                extra={"ошибка": e},
            )
            raise e
        

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        try:
            stmt = select(cls.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            return res.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                f"Ошибка при поиске всех значений в базе данных", extra={"ошибка": e}
            )
            raise e
        

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        try:
            stmt = delete(cls.model).filter_by(id=id).returning(cls.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f'Ошибка при удалении значения из базы данных', extra={'ошибка': e})
            raise e