from typing import Sequence

from sqlalchemy import select

from app.application.protocols.repository import SQLAlchemyRepository
from app.domain.models import Meeting


class MeetingRepository(SQLAlchemyRepository):
    model = Meeting

    async def find_meetings(self, **kwargs) -> Sequence[Meeting]:
        """Поиск всех собраний с заданным условием."""
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalars().all()
