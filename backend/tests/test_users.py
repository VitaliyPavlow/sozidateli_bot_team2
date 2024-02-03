import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "user_data",
    [
        {
            "name": "Вася",
            "phone": "+79999999000",
            "email": "vasya@test.ru",
            "meeting_id": 1,
            "assistance_segment": "Детям в детских домах",
        },
        {
            "name": "Петя",
            "phone": "+79999999001",
            "email": "petya@test.ru",
            "meeting_id": 2,
            "assistance_segment": "Еще не определился",
        },
    ],
)
async def test_create_correct_users(
    async_client: AsyncClient,
    user_data,
    create_meetings,
    check_required_keys_for_users,
):
    response = await async_client.post("/users/", json=user_data)
    data = response.json()
    check_required_keys_for_users([data])
    assert (
        response.status_code == 200
    ), f'Не удалось создать пользователя {user_data["name"]}!'
    data.pop("id")
    assert data == user_data, "Вернулись неправильные данные."


@pytest.mark.parametrize(
    "wrong_users",
    [
        {
            "name": "Black Vlastelin",
            "phone": "phone",
            "email": "black@test.ru",
            "meeting_id": 1,
            "assistance_segment": "Могу автоволонтерить",
        },
        {
            "name": "Black Vlastelin",
            "phone": "+79999999002",
            "email": "black@test",
            "meeting_id": 1,
            "assistance_segment": "Могу автоволонтерить",
        },
        {
            "name": "Black Vlastelin",
            "phone": "+79999999002",
            "email": "black@test.ru",
            "meeting_id": 100,
            "assistance_segment": "Могу автоволонтерить",
        },
        {
            "name": "Black Vlastelin",
            "phone": "+79999999002",
            "email": "black@test.ru",
            "meeting_id": 1,
            "assistance_segment": "Могу пить чай",
        },
        {
            "name": "Black Vlastelin",
            "phone": "+79999999002",
            "email": "black@test.ru",
            "meeting_id": 1,
        },
        {},
    ],
)
async def test_create_incorrect_user(async_client: AsyncClient, wrong_users):
    response = await async_client.post("/users/", json=wrong_users)
    assert response.status_code in (
        400,
        422,
    ), "Неожиданный результат при создании участника с wrong данными."


async def test_get_users(
    async_client: AsyncClient, check_required_keys_for_users
):
    response = await async_client.get("/users/")
    data = response.json()
    assert len(response.json()) == 2, "Неправильно работает метод GET."
    check_required_keys_for_users(data)


async def test_get_user_by_id(
    async_client: AsyncClient, check_required_keys_for_users
):
    response = await async_client.get("/users/1")
    data = response.json()
    check_required_keys_for_users([data])
    assert (
        response.json().get("name") == "Вася"
    ), "Неправильно работает получение данных пользователя по id."


@pytest.mark.parametrize(
    "update_data",
    [
        {"name": "Ирина Вачовски"},
        {"phone": "+79999999003"},
        {"email": "vasya_is_irina_now@test.ru"},
        {"meeting_id": 2},
        {"assistance_segment": "Еще не определился"},
    ],
)
async def test_patch_user_with_valid_data(
    async_client: AsyncClient, update_data, check_required_keys_for_users
):
    key, value = list(update_data.items())[0]
    response = await async_client.patch("/users/1", json=update_data)
    data = response.json()
    check_required_keys_for_users([data])
    assert (
        data.get(key) == value
    ), "Неправильно работает изменение данных участника."


@pytest.mark.parametrize(
    "update_data",
    [
        {"phone": "666"},
        {"email": "vasya_was_here"},
        {"meeting_id": 2000},
        {"assistance_segment": "Гладить котиков"},
    ],
)
async def test_patch_user_with_invalid_data(
    async_client: AsyncClient, update_data
):
    response = await async_client.patch("/users/1", json=update_data)
    assert response.status_code in (
        400,
        422,
    ), "Неправильное поведение при обновлении некорректными данными"
