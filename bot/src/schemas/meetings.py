from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .users import GetUser


class MeetingCreate(BaseModel):
    date: datetime
    description: str


class GetMeeting(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: datetime
    is_open: bool
    description: str


class MeetingUpdate(BaseModel):
    date: datetime | None = None
    is_open: bool | None = None
    description: str | None = None


class MeetingParticipants(BaseModel):
    id: int
    date: datetime
    is_open: bool
    description: str
    users: list[GetUser]
