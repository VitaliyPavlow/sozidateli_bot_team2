import os
from dataclasses import dataclass


@dataclass
class Settings:
    bot_token: str = os.getenv('BOT_TOKEN')
    throttle_time_spin: int = os.getenv('THROTTLE_TIME_SPIN')
    throttle_time_other: int = os.getenv('THROTTLE_TIME_OTHER')
    manager_chat_id: int = os.getenv('MANAGER_CHAT_ID')
    url: str = os.getenv('URL', 'http://localhost:8000')
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
