#!/bin/bash

sleep 5

alembic upgrade head || 0

exec "$@"
