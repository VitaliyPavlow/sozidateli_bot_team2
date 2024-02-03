# Запуск backend сервиса

## Локальный запуск

1) Установить необходимую версию python: 3.11

2) Создать виртуальное окружение в проекте:

  * linux: `python -m venv venv`

  * Windows: `py -m venv venv`

3) Активировать виртуальное окружение:

    * linux: `. venv/bin/activate`

    * windows: `. venv\Scripts\activate`

4) Создать необходимые зависимости: `pip install -r requirements.txt`

5) Запустить сервер: `uvicorn app.main:app`

## Запуск через докер

1) Установить докер:

    * Для linux: [docker](https://docs.docker.com/engine/install/ubuntu/)

    * Для windows: [docker](https://docs.docker.com/desktop/install/windows-install/)

2) Запустить проект:

`docker build -t sozidateli .`

`docker run --name sozidateli_container --rm -p 8000:8080 sozidateli`
