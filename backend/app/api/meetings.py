from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.application.services import MeetingServices
from app.core.exceptions import (
    InvalidDate,
    MeetingClosed,
    ObjectIsNoneException,
)
from app.domain.schemas import (
    GetMeeting,
    MeetingCreate,
    MeetingParticipants,
    MeetingUpdate,
)
from .dependencies import UoWDep

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.get(
    "/", response_model=list[GetMeeting], summary="Получить список собраний."
)
async def get_meetings(uow: UoWDep):
    """Получение списка всех собраний."""
    return await MeetingServices().get_meetings(uow)


@router.get("/{id}", response_model=GetMeeting, summary="Получить собрание.")
async def get_meeting(id: int, uow: UoWDep):
    """Получить собрание."""
    try:
        return await MeetingServices().get_meeting(uow, id)
    except AttributeError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Собрание с id = {id} отсутствует."
        )


@router.post("/", response_model=GetMeeting, summary="Создание собрания.")
async def create_meeting(uow: UoWDep, meeting: MeetingCreate):
    """Создать собрание."""
    try:
        return await MeetingServices().create_meeting(uow, meeting)
    except InvalidDate as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        )


@router.patch(
    "/{id}", response_model=GetMeeting, summary="Редактирование собрания."
)
async def update_meeting(uow: UoWDep, id: int, meeting: MeetingUpdate):
    """Обновление собрания."""
    try:
        return await MeetingServices().update_meeting(uow, id, meeting)
    except (InvalidDate, ObjectIsNoneException, MeetingClosed) as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        )


@router.delete(
    "/{id}", response_model=GetMeeting, summary="Удалить собрание."
)
async def delete_meeting(uow: UoWDep, id: int):
    """Удалить собрание с указанным id."""
    try:
        return await MeetingServices().delete_meeting(uow, id)
    except (ObjectIsNoneException, MeetingClosed) as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        )


@router.get(
    "/{id}/participants",
    response_model=MeetingParticipants,
    summary="Список записавшихся на собрание.",
)
async def get_participants_list(uow: UoWDep, id: int):
    """Получение списка записавшихся на собрание."""
    try:
        return await MeetingServices().get_participants(uow, id)
    except ObjectIsNoneException() as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        )

@router.get("/close/")
async def close_meetings(uow: UoWDep) -> None:
    """Закрытие собраний."""
    await MeetingServices().close_meeting(uow)
