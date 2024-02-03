import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "meetings",
    [
        {
            "date": "2034-02-02T15:25:04.424Z",
            "description": "Собрание модных обжэшников.",
        },
        {
            "date": "2034-02-03T15:25:04.424Z",
        },
    ],
)
async def test_create_correct_meetings(
    async_client: AsyncClient, meetings, check_required_keys_for_meetings
):
    response = await async_client.post("/meetings/", json=meetings)
    data = response.json()
    check_required_keys_for_meetings([data])
    assert (
        response.status_code == 200
    ), f'Не удалось создать собрание {meetings["date"]}!'
    assert data["date"][:-3] == meetings["date"][:-1]


@pytest.mark.parametrize(
    "wrong_meetings",
    [{"date": "2024-02-01T15:25:04.424Z"}, {}],
)
async def test_create_incorrect_meetings(
    async_client: AsyncClient, wrong_meetings
):
    response = await async_client.post("/meetings/", json=wrong_meetings)
    assert response.status_code in (400, 422), "Неожиданное поведение."


async def test_get_meetings(
    async_client: AsyncClient, check_required_keys_for_meetings
):
    response = await async_client.get("/meetings/")
    data = response.json()
    check_required_keys_for_meetings(data)
    assert response.status_code == 200


async def test_get_meeting_by_id(
    async_client: AsyncClient, check_required_keys_for_meetings
):
    response = await async_client.get("/meetings/1")
    data = response.json()
    check_required_keys_for_meetings([data])
    assert response.json().get("date") == "2034-02-02T15:25:04.424000"


@pytest.mark.parametrize(
    "meetings",
    [
        {"date": "2032-02-02T15:25:04.424Z"},
        {"description": "Это какое-то новое описание."},
    ],
)
async def test_patch_meeting_with_valid_data(
    async_client: AsyncClient, meetings, check_required_keys_for_meetings
):
    response = await async_client.patch("/meetings/1", json=meetings)
    data = response.json()
    check_required_keys_for_meetings([data])
    assert response.status_code == 200
    assert (
        data["date"] == "2032-02-02T15:25:04.424000"
    ), "При обновлении получены неправильные данные."


@pytest.mark.parametrize(
    "wrong_meetings", [{"date": "2012-02-02T15:25:04.424Z"}]
)
async def test_patch_meeting_with_invalid_data(
    async_client: AsyncClient, wrong_meetings
):
    response = await async_client.patch("/meetings/1", json=wrong_meetings)
    assert response.status_code in (
        400,
        422,
    ), "Неожиданное поведение при неправильных данных."


async def test_delete_meeting(async_client: AsyncClient):
    response = await async_client.delete("/meetings/2")
    assert response.status_code == 200, "Ошибка при удалении собрания."


async def test_get_participants_of_meeting(
    async_client: AsyncClient, create_participants
):
    required_keys = ["date", "is_open", "id", "description", "users"]
    required_keys_user = [
        "name",
        "phone",
        "email",
        "meeting_id",
        "id",
        "assistance_segment",
    ]
    response = await async_client.get("/meetings/1/participants")
    meeting = response.json()
    users = meeting["users"]
    assert (
        len(response.json().get("users")) == 2
    ), "Неправильное количество пользователей."
    assert all(
        key in meeting for key in required_keys
    ), "Отсутствуют необходимые ключи в полученных данных."
    for user in users:
        assert all(
            key in user for key in required_keys_user
        ), "Отсутствуют необходимые ключи в полученных данных."
