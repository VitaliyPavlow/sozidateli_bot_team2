from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    declared_attr,
    mapped_column,
)

from app.core import settings

engine = create_async_engine(url=settings.db_url, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

    def __str__(self):
        return self.__tablename__


Base = declarative_base(cls=Base)
