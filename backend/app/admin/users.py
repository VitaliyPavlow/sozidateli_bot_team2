from dataclasses import dataclass
from typing import Any

from starlette.requests import Request
from starlette_admin import (
    EmailField,
    EnumField,
    HasOne,
    PhoneField,
    StringField,
)
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.exceptions import FormValidationError

from app.application.repositories.users import UserRepository
from app.domain.models import User
from app.domain.models.enums import AssistanceSegment


@dataclass
class EnumCustomField(EnumField):
    """Кастомный enum для полей."""

    def _get_label(self, value: Any, request: Request) -> Any:
        for v, label in self._get_choices(request):
            if value == getattr(AssistanceSegment, v):
                return label
        raise ValueError(f"Invalid choice value: {value}")


class UserView(ModelView):
    """
    Модель отображения записавшихся пользователей в админке.
    """

    identity = "user"
    fields = [
        StringField("name", label="Имя", required=True),
        PhoneField("phone", label="Номер телефона", required=True),
        EmailField("email", required=True),
        EnumCustomField(
            "assistance_segment",
            label="Направление помощи",
            choices=[("children_in_hospital", "Детям в больницах"),
                     ("children_in_orphanages", "Детям в детских домах"),
                     ("disabled_children", "Семьям с детьми-инвалидами"),
                     ("auto_volunteer", "Могу автоволонтерить"),
                     ("not_decide", "Еще не определился")],
            required=True
        ),
        HasOne(
            "meeting", label="Собрание", identity="meeting", required=True
        ),
    ]
    label = "Участники"
    sortable_fields = [User.meeting]

    async def validate(self, request: Request, data: dict[str, Any]) -> None:
        """Валидация полей."""
        errors: dict[str, str] = dict()
        if data["assistance_segment"] is None:
            errors["assistance_segment"] = "Нужно выбрать направление помощи."
        if data["meeting"] is None:
            errors["meeting"] = "Нужно выбрать собрание."
        if data["phone"] is None:
            errors["phone"] = "Нужно указать номер телефона."
        if data["name"] is None:
            errors["name"] = "Нужно указать имя участника."
        if data["email"] is None:
            errors["email"] = "Нужно укзать почту."

        try:
            data["meeting_id"] = data["meeting"].id
        except AttributeError:
            data["meeting_id"] = None

        if request.state.action == "CREATE":
            await self._validate_create(request, data, errors)

        if len(errors) > 0:
            raise FormValidationError(errors)

        self._change_assistance_segment(data)

        await super().validate(request, data)

    async def _validate_create(self,
                               request: Request,
                               data: dict[str, Any],
                               errors: dict[str, str]) -> None:
        user_attrs = {
            "email": "Пользователя с данной почтой уже существует.",
            "phone": "Пользователь с данным телефоном уже существует."
        }
        for key, value in user_attrs.items():
            if await UserRepository(
                    request.state.session
            ).check_user_exists(
                **{key: data[key]}, meeting_id=data["meeting_id"]
            ):
                errors[key] = value

    def _change_assistance_segment(self, data: dict[str, Any]) -> None:
        data["assistance_segment"] = getattr(
            AssistanceSegment, data["assistance_segment"]
        )
