from abc import ABC, abstractmethod
from typing import Any, Sequence, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db import Base

ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepository(ABC):
    """Абстрактный класс репозитория."""

    @abstractmethod
    async def add_one(self):
        """Добавление данных."""

    @abstractmethod
    async def update_one(self, id: int):
        """Обновление данных."""

    @abstractmethod
    async def find_one(self):
        """Поиск элемента."""

    @abstractmethod
    async def find_all(self):
        """Поиск элементов."""

    @abstractmethod
    async def delete_one(self):
        """Удаление элемента."""


class SQLAlchemyRepository(AbstractRepository):
    """Класс репозитория для SQLAlchemy."""
    model: ModelType | None = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, **kwargs: dict[str, Any]) -> ModelType:
        """Добавление данных в БД."""
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update_one(
            self, id: int, **kwargs: dict[str, Any]
    ) -> ModelType:
        """Обновление данных в БД."""
        stmt = update(
            self.model
        ).values(**kwargs).filter_by(id=id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def find_one(
            self, **filter_by: dict[str, Any]
    ) -> ModelType | None:
        """Поиск записи в БД."""
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all(self) -> Sequence[ModelType]:
        """Поиск записей в БД."""
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_one(self, **filter_by: dict[str, Any]) -> ModelType:
        """Удаление записи в БД."""
        stmt = delete(
            self.model
        ).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()
