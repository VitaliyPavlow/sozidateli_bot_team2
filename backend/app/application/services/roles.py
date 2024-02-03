from app.application.protocols.unit_of_work import UoW

from sqlalchemy.exc import IntegrityError


class RoleService:
    async def create_roles(self, uow: UoW):
        """Создание ролей"""
        roles = ("read",
                 "create",
                 "edit",
                 "delete",
                 "action_make_published")
        async with uow:
            try:
                await uow.roles.create_roles(roles)
                await uow.commit()
            except IntegrityError:
                # Создание ролей должно происходить один раз.
                pass
