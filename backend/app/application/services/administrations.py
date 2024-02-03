from app.application.protocols.unit_of_work import UoW
from app.core.password import get_password_hash
from sqlalchemy.exc import IntegrityError


class AdministrationsService:
    async def create_admin(self, uow: UoW, data: dict[str, str]) -> None:
        async with uow:
            data["password"] = get_password_hash(data["password"])
            try:
                user = await uow.administrations.add_one(**data)
                user.roles = await uow.roles.find_all()
                await uow.commit()
            except IntegrityError:
                """Если пользователь уже создан, 
                то исключение игнорируется."""
                pass
