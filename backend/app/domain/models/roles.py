from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.infrastructure.db import Base
from .association_tables import administration_roles


class Role(Base):
    """Модель ролей."""

    name: Mapped[str] = mapped_column(unique=True)
    administrations: Mapped[list["Administration"]] = relationship(
        secondary=administration_roles, back_populates='roles'
    )
