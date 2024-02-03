from app.application.protocols.unit_of_work import UoW
from app.core.exceptions import UserAlreadyExists, ObjectIsNoneException
from app.domain.schemas import GetUser, UserCreate, UserUpdate
from .base import BaseService


class UserService(BaseService):
    async def get_users(self, uow: UoW) -> list[GetUser]:
        """Получить список пользователей."""
        async with uow:
            users = await uow.users.find_all()
            return [user.to_read_model() for user in users]

    async def get_user(self, uow: UoW, id: int) -> GetUser:
        """Получить пользователя по id."""
        async with uow:
            user = await uow.users.find_one(id=id)
            return user.to_read_model()

    async def create_user(self, uow: UoW, schema: UserCreate) -> GetUser:
        """Создать пользователя."""
        async with uow:
            await self._validate_user_exists(
                uow, schema.phone, schema.meeting_id, schema.email
            )
            await self._check_meeting(schema.meeting_id, uow)
            user = await uow.users.add_one(**schema.model_dump())
            await uow.commit()
            return user.to_read_model()

    async def update_user(
            self, uow: UoW, id: int, schema: UserUpdate
    ) -> GetUser:
        """Обновить информацию о пользователе."""
        async with uow:
            await self._validate_user_exists(
                uow, schema.phone, schema.meeting_id
            )
            if schema.meeting_id:
                await self._check_meeting(schema.meeting_id, uow)
            user = await uow.users.update_one(
                id=id, **schema.model_dump(exclude_none=True)
            )
            await uow.commit()
            return user.to_read_model()

    async def delete_user(self, uow: UoW, id: int) -> GetUser:
        """Удалить пользователя."""
        async with uow:
            await self._check_user(uow, id)
            user = await uow.users.delete_one(id=id)
            await uow.commit()
            return user.to_read_model()

    async def _validate_user_exists(
            self,
            uow: UoW,
            phone: str | None = None,
            meeting_id: int | None = None,
            email: str | None = None
    ) -> None:
        """Проверка уникальности пользователя."""
        if meeting_id and phone and email:
            values = {'email': email,
                      'phone': phone}
            for key, value in values.items():
                user = await uow.users.find_one(**{key: value})
                if user and user.meeting_id == meeting_id:
                    raise UserAlreadyExists()

    async def _check_user(self, uow: UoW, id: int) -> None:
        if not await uow.users.find_one(id=id):
            raise ObjectIsNoneException()
