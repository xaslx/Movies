from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.favorite import Favorite


class User(Base):
    __tablename__ = 'users'


    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    registered_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


    favorites: Mapped[list['Favorite']] = relationship('Favorite', back_populates='user')