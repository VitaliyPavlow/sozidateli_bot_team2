from pydantic import BaseModel, ConfigDict, EmailStr, Field


class GetUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    email: EmailStr
    meeting_id: int


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    phone: str
    email: EmailStr
    meeting_id: int
    assistance_segment: str


class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    meeting_id: int | None = None
