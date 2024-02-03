import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Настройки проекта."""

    db_url: str = os.getenv("DB_URL", "sqlite+aiosqlite:///sqlite.db")
    app_title: str = "API для проекта 'Созидатели'."
    admin_panel_password: str = os.getenv("ADMIN_PANEL_PASSWORD", "password")
    admin_middleware_secret: str = os.getenv(
        "ADMIN_MIDDLEWARE_SECRET", "1234567890"
    )
