from sqlalchemy import select

from app.application.protocols.repository import SQLAlchemyRepository
from app.domain.models.administrations import Administration


class AdministrationRepository(SQLAlchemyRepository):
    model = Administration

    async def check_user_exists(self, **filter_by) -> bool:
        stmt = select(self.model).filter_by(**filter_by).exists()
        return await self.session.scalar(select(stmt))
