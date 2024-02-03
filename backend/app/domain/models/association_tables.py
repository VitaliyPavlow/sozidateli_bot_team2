from sqlalchemy import ForeignKey, Table, Column

from app.infrastructure.db import Base

administration_roles = Table(
    "administration_roles",
    Base.metadata,
    Column("administration_id", ForeignKey("administration.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True),
)
