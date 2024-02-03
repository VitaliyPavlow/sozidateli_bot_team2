from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.application.services import UserService
from app.core.exceptions import (
    MeetingClosed,
    UserAlreadyExists,
    ObjectIsNoneException,
)
from app.domain.schemas import GetUser, UserCreate, UserUpdate
from .dependencies import UoWDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=list[GetUser],
    summary="Получить список пользователей."
)
async def get_users(uow: UoWDep):
    """Получить список пользователей."""
    return await UserService().get_users(uow)


@router.get("/{id}", response_model=GetUser)
async def get_user(id: int, uow: UoWDep):
    """Получение пользователя."""
    try:
        return await UserService().get_user(uow, id)
    except AttributeError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Пользователь с id = {id} отсутствует."
        )


@router.post("/", response_model=GetUser, summary="Создать пользователя.")
async def create_user(user: UserCreate, uow: UoWDep):
    """Создать пользователя."""
    try:
        return await UserService().create_user(uow, user)
    except MeetingClosed:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Запись на собрание уже закрыта.",
        )
    except (ObjectIsNoneException, UserAlreadyExists) as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        )


@router.patch(
    "/{id}", response_model=GetUser, summary="Обновить пользователя."
)
async def update_user(user: UserUpdate, uow: UoWDep, id: int):
    """Редавктировать инфо о пользователе."""
    try:
        return await UserService().update_user(uow, id, user)
    except (UserAlreadyExists, ObjectIsNoneException) as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        )
    except MeetingClosed:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Запись на собрание уже закрыта.",
        )


@router.delete(
    "/{id}", response_model=GetUser, summary="Удалить пользователя."
)
async def delete_user(uow: UoWDep, id: int):
    """Удалить пользователя."""
    try:
        return await UserService().delete_user(uow, id)
    except ObjectIsNoneException as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        )
