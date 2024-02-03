import datetime as dt

from pydantic import BaseModel, ConfigDict

from .users import GetUser


class BaseMeeting(BaseModel):
    """Базовая схема собрания."""

    date: dt.datetime | None = None
    is_open: bool | None = None
    description: str | None = None


class MeetingCreate(BaseModel):
    """Схема создания собрания."""

    date: dt.datetime
    description: str | None = None


class GetMeeting(BaseMeeting):
    """Схема получения собрания."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    date: dt.datetime
    is_open: bool


class MeetingUpdate(BaseMeeting):
    """Схема обновления собрания."""

    ...


class MeetingParticipants(BaseModel):
    """Схема собрания с пользователями."""

    id: int
    date: dt.datetime
    is_open: bool
    description: str
    users: list[GetUser]
