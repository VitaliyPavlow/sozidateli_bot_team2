from app.application.protocols.repository import SQLAlchemyRepository
from app.domain.models.roles import Role
from sqlalchemy import insert


class RoleRepository(SQLAlchemyRepository):
    model = Role

    async def create_roles(self, roles: tuple[str, ...]) -> None:
        """Создание ролей."""
        for role in roles:
            stmt = insert(self.model).values(name=role)
            await self.session.execute(stmt)
