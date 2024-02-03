from sqlalchemy import select

from app.application.protocols.repository import SQLAlchemyRepository
from app.domain.models.users import User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def check_user_exists(self, **filter_by) -> bool:
        """Проверка имеющегося пользователя в базе данных."""
        stmt = select(self.model).filter_by(**filter_by).exists()
        return await self.session.scalar(select(stmt))
