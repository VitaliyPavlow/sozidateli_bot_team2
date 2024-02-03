from pydantic import BaseModel


class BaseRole(BaseModel):
    """Схема ролей."""

    name: str
