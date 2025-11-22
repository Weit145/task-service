import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
class Settings(BaseSettings):
    broker: str = os.getenv("CELERY_BROKER", "default_broker")
    sender_email: str = os.getenv("YANDEX_USER", "default_email")
    app_password: str = os.getenv("YANDEX_APP_PASSWORD", "default_password")
    
    kafka_url: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS","kafka:9092")

settings = Settings()