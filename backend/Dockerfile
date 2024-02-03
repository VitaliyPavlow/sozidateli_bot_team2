FROM python:3.11

WORKDIR /app

COPY prod.txt requirements.txt

RUN pip install gunicorn
RUN pip install -r requirements.txt --no-cache-dir

COPY app ./app
COPY alembic.ini alembic.ini
COPY alembic ./alembic
COPY --chmod=0755 scripts/create_migrations.sh /usr/local/bin/

ENTRYPOINT ["/usr/local/bin/create_migrations.sh"]
CMD gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080
