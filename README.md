# Созидатели

«Созидатели» — это команда отзывчивых людей, и более 10 лет помогаем самой социально не защищенной категории — детям. За
плечами многолетний опыт волонтерства, координирования социальных проектов, выстраивания системы помощи детям.

# Технологии

* python3.11

* FastAPI

* SQLAlchemy

* Pydantic

* PostgreSQL

* Alembic

* Aiogram

* aiohttp

# Установка

1. Клонировать репозиторий: `git@github.com:Studio-Yandex-Practicum/sozidateli_bot_team2.git`

2. Установить докер:

    * Для linux: [docker](https://docs.docker.com/engine/install/ubuntu/)

    * Для windows: [docker](https://docs.docker.com/desktop/install/windows-install/)

3. Создать в корне проекта файл `.env` с параметрами:

    * `DB_URL=postgresql+asyncpg://postgres:password@postgresql:5432/users` - URL-адрес подключения к базе данных

    * `BOT_TOKEN=TOKEN` - токен Telegram

    * `THROTTLE_TIME_SPIN=2` и `THROTTLE_TIME_OTHER=1` - параметры тротлинга

    * `POSTGRES_USER=postgres`, `POSTGRES_PASSWORD=password`, `POSTGRES_DB=users` - доступы к базе данных

    * `ADMIN_PANEL_USER=admin` - юзернейм для первого создания админа

    * `ADMIN_PANEL_PASSWORD=password` - пароль для первого создания админа

    * `ADMIN_MIDDLEWARE_SECRET=SECRET` - секретный ключ доступа
   
    * `MANAGER_CHAT_ID=CHAT_ID` - ID-чат координатора

    * `URL=http://localhost:80800` - адрес backend-сервиса

    * `REDIS_HOST=localhost` - хост от Redis

4. Запуск проекта: `docker compose up --build`

5. Вход в админку по адресу: `https://{URL}/admin`

# Лицензия

[MIT](https://github.com/Studio-Yandex-Practicum/sozidateli_bot_team2?tab=MIT-1-ov-file)
