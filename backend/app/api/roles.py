from fastapi import APIRouter

from .dependencies import UoWDep
from app.application.services.roles import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/")
async def create_roles(uow: UoWDep) -> None:
    """Создание ролей."""
    await RoleService().create_roles(uow)
