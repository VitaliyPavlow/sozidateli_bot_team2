import pytest
from httpx import AsyncClient


@pytest.fixture
async def create_participants(async_client: AsyncClient):
    participant_1 = {
        "name": "Вася",
        "phone": "+79999999000",
        "email": "vasya@test.ru",
        "meeting_id": 1,
        "assistance_segment": "Детям в детских домах",
    }
    participant_2 = {
        "name": "Петя",
        "phone": "+79999999001",
        "email": "petya@test.ru",
        "meeting_id": 1,
        "assistance_segment": "Еще не определился",
    }
    await async_client.post("/users/", json=participant_1)
    await async_client.post("/users/", json=participant_2)
    yield
    await async_client.delete("/users/1")
    await async_client.delete("/users/2")


@pytest.fixture
async def create_meetings(async_client: AsyncClient):
    meeting1 = {
        "date": "2070-02-02T12:55:36.672Z",
        "description": "Hello from future",
    }
    meeting2 = {
        "date": "2070-02-03T12:55:36.672Z",
        "description": "Hello from future 2",
    }
    await async_client.post("/meetings/", json=meeting1)
    await async_client.post("/meetings/", json=meeting2)
    yield


@pytest.fixture
def check_required_keys_for_meetings():
    required_keys = ["date", "is_open", "id", "description"]

    def _check_required_keys(data):
        for item in data:
            assert all(
                key in item for key in required_keys
            ), "Отсутствуют необходимые ключи в полученных данных."

    return _check_required_keys


@pytest.fixture
def check_required_keys_for_users():
    required_keys = [
        "name",
        "phone",
        "email",
        "meeting_id",
        "id",
        "assistance_segment",
    ]

    def _check_required_keys(data):
        for item in data:
            assert all(
                key in item for key in required_keys
            ), "Отсутствуют необходимые ключи в полученных данных."

    return _check_required_keys
