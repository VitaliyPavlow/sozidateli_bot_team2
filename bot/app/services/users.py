import logging
from collections.abc import Generator
from http import HTTPStatus
from pathlib import Path

import aiohttp
from aiohttp import ClientResponse

from core import settings
from core.logging_config import configure_logging
from schemas import users
from services.exceptions import HTTPRequestError

configure_logging(Path(__file__).parent / 'logs')


class UserService:
    def __init__(self):
        self._path = '/users'

    async def get_users(self) -> Generator[users.GetUser]:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.get(self._path) as response:
                logging.info('Получение списка пользователей')
                return await self._get_users(response)

    async def create_user(self, user: users.UserCreate) -> users.GetUser:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.post(self._path,
                                    json=user.model_dump()) as response:
                logging.info('Создание пользователя')
                return await self._get_user(response)

    async def update_user(self, id: int,
                          user: users.UserUpdate) -> users.GetUser:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.post(f'self._path/{id}',
                                    json=user.model_dump()) as response:
                logging.info('Обновление пользователя')
                return await self._get_user(response)

    async def delete_user(self, id: int):
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.delete(f'{self._path}/{id}') as response:
                if not (response.status == HTTPStatus.OK):
                    res = await response.json()
                    logging.error('Не удалось удалить пользователя')
                    raise HTTPRequestError(
                        f'Ошибка запроса: {res["detail"]}'
                    )

    async def _get_user(self,
                        response: ClientResponse) -> users.GetUser:
        if response.status == HTTPStatus.OK:
            logging.info('Пользователь получен')
            return users.GetUser(**(await response.json()))
        res = await response.json()
        logging.error('Не удалось получить пользователя')
        raise HTTPRequestError(
            f'Ошибка запроса: {res["detail"]}'
        )

    async def _get_users(
            self, response: ClientResponse
    ) -> Generator[users.GetUser]:
        if response.status == HTTPStatus.OK:
            logging.info('Список пользователей получен')
            return (users.GetUser(**json) for json in
                    await response.json())
        res = await response.json()
        logging.error('Не удалось получить список пользователей')
        raise HTTPRequestError(
            f'Ошибка запроса: {res["detail"]}'
        )
