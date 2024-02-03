from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.ext.asyncio import async_sessionmaker

from app.application.repositories import (MeetingRepository,
                                          UserRepository,
                                          RoleRepository,
                                          AdministrationRepository)


class UoW(ABC):
    """Абстрактный класс паттерна UnitOfWork."""
    users = Type[UserRepository]
    meetings = Type[MeetingRepository]
    roles = Type[RoleRepository]
    administrations = Type[AdministrationRepository]

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(UoW):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.meetings = MeetingRepository(self.session)
        self.roles = RoleRepository(self.session)
        self.administrations = AdministrationRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
