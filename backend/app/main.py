from fastapi import FastAPI
from httpx import AsyncClient

from app.admin.admin import admin
from app.api import routers
from app.core import Settings
from app.core.decorators import repeat_every


def create_app() -> FastAPI:
    """Фабрика FastAPI."""

    app = FastAPI(title=Settings.app_title)
    admin.mount_to(app)

    for router in routers:
        app.include_router(router)

    return app


app = create_app()


@app.on_event("startup")
async def create_roles():
    async with AsyncClient(app=app, base_url="http://app") as client:
        await client.get('/roles/')


@app.on_event("startup")
async def create_admin():
    async with AsyncClient(app=app, base_url="http://app") as client:
        await client.get('/create_admin_user/')


@app.on_event("startup")
@repeat_every(60)
async def close_meetings():
    """Закрытие собраний."""
    async with AsyncClient(app=app, base_url="http://app") as client:
        await client.get('/meetings/close/')
