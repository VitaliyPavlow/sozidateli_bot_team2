import logging
from collections.abc import Generator
from http import HTTPStatus
from pathlib import Path

import aiohttp
from aiohttp import ClientResponse

from core import settings
from core.logging_config import configure_logging
from schemas import meetings
from services.exceptions import HTTPRequestError

configure_logging(Path(__file__).parent / 'logs')


class MeetingService:
    def __init__(self):
        self._path = '/meetings'

    async def get_meetings(self) -> Generator[meetings.GetMeeting]:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.get(self._path) as response:
                logging.info('Получение списка встреч')
                return await self._get_meetings(response)

    async def create_meeting(
            self, meeting: meetings.MeetingCreate
    ) -> meetings.GetMeeting:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.post(
                    self._path, json=meeting.model_dump()
            ) as response:
                if response.status == HTTPStatus.OK:
                    logging.info('Встреча создана')
                    return meetings.GetMeeting(**(await response.json()))
                res = await response.json()
                logging.error('Не удалось создать встречу')
                raise HTTPRequestError(
                    f'Ошибка запроса: {res["detail"]}'
                )

    async def update_meeting(
            self,
            id: int,
            meeting: meetings.MeetingUpdate
    ) -> meetings.GetMeeting:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.patch(
                    f'{self._path}/{id}', json=meeting.model_dump()
            ) as response:
                logging.info('Встреча обновлена')
                return await self._get_meeting(response)

    async def delete_meeting(self, id: int):
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.delete(f'{self._path}/{id}') as response:
                if not (response.status == HTTPStatus.OK):
                    res = await response.json()
                    logging.error('Не удалось удалить встречу')
                    raise HTTPRequestError(
                        f'Ошибка запроса: {res["detail"]}.'
                    )

    async def get_participants_list(self, id: int):
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.get(
                    f'{self._path}/{id}/participants') as response:
                if response.status == HTTPStatus.OK:
                    logging.info('Список участников получен')
                    return meetings.MeetingParticipants(
                        **(await response.json()))
                res = await response.json()
                logging.error('Не удалось получить список участников')
                raise HTTPRequestError(
                    f'Ошибка запроса: {res["detail"]}'
                )

    async def _get_meeting(self,
                           response: ClientResponse) -> meetings.GetMeeting:
        if response.status == HTTPStatus.OK:
            logging.info('Встреча получена')
            return meetings.GetMeeting(**(await response.json()))
        res = await response.json()
        logging.error('Не удалось получить встречу')
        raise HTTPRequestError(
            f'Ошибка запроса: {res["detail"]}'
        )

    async def _get_meetings(
            self, response: ClientResponse
    ) -> Generator[meetings.GetMeeting]:
        if response.status == HTTPStatus.OK:
            logging.info('Список встреч получен')
            return (meetings.GetMeeting(**json) for json in
                    await response.json())
        res = await response.json()
        logging.error('Не удалось получить список встреч')
        raise HTTPRequestError(
            f'Ошибка запроса: {res["detail"]}'
        )
