from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.infrastructure.db import Base
from .association_tables import administration_roles


class Administration(Base):
    """Модель администратора."""

    name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    roles: Mapped[list["Role"]] = relationship(
        secondary=administration_roles,
        back_populates="administrations",
        lazy="selectin"
    )
