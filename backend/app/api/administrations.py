from fastapi import APIRouter

from .dependencies import UoWDep

from app.core import Settings
from app.application.services.administrations import AdministrationsService

router = APIRouter(prefix="/create_admin_user", tags=["Administrations"])


@router.get("/")
async def create_admin(uow: UoWDep) -> None:
    data = {"name": "admin",
            "username": "admin",
            "password": Settings.admin_panel_password}
    await AdministrationsService().create_admin(uow, data)
