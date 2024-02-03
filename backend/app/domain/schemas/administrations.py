from pydantic import BaseModel, field_validator

from app.core.constants import USERNAME_LENGTH, PASSWORD_LENGTH


class BaseAdministration(BaseModel):
    name: str
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if len(value) < USERNAME_LENGTH:
            raise ValueError(
                f"Юзернейм должен быть больше {USERNAME_LENGTH} символов."
            )
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < PASSWORD_LENGTH:
            raise ValueError(
                f"Пароль должен быть больше {PASSWORD_LENGTH} символов."
            )
        return value



