from typing import Any, Dict

from starlette.requests import Request
from starlette_admin import HasMany, StringField, PasswordField
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.exceptions import FormValidationError
from app.application.repositories import AdministrationRepository

from app.core.password import get_password_hash


class AdministrationView(ModelView):
    """Модель для отображения админов в админке."""

    identity = "administration"

    fields = [
        StringField("name", label="Имя пользователя", required=True),
        StringField("username", label="юзернейм", required=True),
        PasswordField("password", label="пароль", required=True),
        HasMany("roles", label="Параметры", identity="role", required=True)
    ]

    label = "Администрация"
    sortable_fields = ["name", "username"]
    fields_default_sort = ["name"]

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        """Валидация полей."""
        errors: dict[str, str] = dict()

        if data["name"] is None:
            errors["name"] = "Нужно указать имя."

        if data["username"] is None:
            errors["username"] = "Нужно указать юзернейм."

        if data["password"] is None:
            errors["password"] = "Нужно указать пароль."

        if len(data["roles"]) == 0:
            errors["roles"] = "Нужно указать роль пользователю."

        if len(errors) > 0:
            raise FormValidationError(errors)

        if request.state.action == "CREATE":
            await self._validate_create(request, data["username"], errors)

        data["password"] = self._password_hash(data["password"])

        await super().validate(request, data)

    async def _validate_create(self,
                      request: Request,
                      username: str,
                      errors: dict[str, Any] ) -> None:
        if await AdministrationRepository(
                request.state.session
        ).check_user_exists(username=username):
            errors["username"] = ("Пользователь с таким "
                                  "юзернеймом уже существует.")

    def _password_hash(self, password: str) -> str:
        return get_password_hash(password)
