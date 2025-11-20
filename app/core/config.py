import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    broker: str = os.getenv("CELERY_BROKER_URL", "default_broker")
    sender_email: str = os.getenv("YANDEX_USER", "default_email")
    app_password: str = os.getenv("YANDEX_APP_PASSWORD", "default_password")

settings = Settings()