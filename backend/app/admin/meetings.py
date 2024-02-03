import datetime as dt
from typing import Any
from zoneinfo import ZoneInfo

from starlette.requests import Request
from starlette_admin import (
    BooleanField,
    DateTimeField,
    HasMany,
    TextAreaField,
)
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.exceptions import FormValidationError

from app.core.constants import ZONEINFO


class MeetingView(ModelView):
    """Модель для отображения собраний в админке."""

    identity = "meeting"

    fields = [
        DateTimeField("date", label="Дата и время"),
        BooleanField("is_open", label="Закрыто/Открыто"),
        TextAreaField("description", label="Описание собрания"),
        HasMany("users", label="Участники собрания", identity="user"),
    ]
    label = "Собрания"
    sortable_fields = ["date", "is_open"]
    fields_default_sort = ["date", ("is_open", True)]

    async def validate(self, request: Request, data: dict[str, Any]) -> None:
        """Валидация полей."""
        errors: dict[str, str] = dict()

        if data["date"] is None:
            errors["date"] = "Нужно указать дату собрания."

        if data["date"] and data["date"].replace(
                tzinfo=ZoneInfo(ZONEINFO)
        ).timestamp() < dt.datetime.now(
                tz=ZoneInfo(ZONEINFO)
        ).timestamp():
            errors["date"] = "Дата собрания не может быть меньше текущей."

        if len(errors) > 0:
            raise FormValidationError(errors)

        await super().validate(request, data)
