import os
from dotenv import load_dotenv

load_dotenv()

class ConfigManager:
    def __init__(self) -> None:
        self.POSTGRES_USER: str = self._get_required_env("POSTGRES_USER")
        self.POSTGRES_PASSWORD: str = self._get_required_env("POSTGRES_PASSWORD")
        self.POSTGRES_DB: str = self._get_required_env("POSTGRES_DB")
        self.POSTGRES_HOST: str = self._get_required_env("POSTGRES_HOST")
        self.POSTGRES_PORT: str = self._get_required_env("POSTGRES_PORT")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE: str = self._get_required_env("LOG_FILE")
        self.RABBITMQ_HOST: str = self._get_required_env("RABBITMQ_HOST")
        self.WORKER_METRICS_URL: str = self._get_required_env("WORKER_METRICS_URL")

    def _get_required_env(self, key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Missing required environment variable: {key}")
        return value

    def get_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = ConfigManager()
