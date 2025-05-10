from typing import List, Dict, Any
from aiogram.types import BotCommand
from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    NAME: str
    HOST: str
    PORT: int
    PASSWORD: str
    USER: str

    @property
    def URL(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

    class Config:
        env_prefix = 'POSTGRES_'
        env_file = '.env'
        extra = 'ignore'


class BotConfig(BaseSettings):
    TOKEN: str
    GROUP_ID: int
    COMMISSION: float
    PARTNERS: List[Dict[str, Any]]
    ADMINS: list[int] | None = []
    SUPPORT_LINK: str
    COMMANDS: list[BotCommand] = [
        BotCommand(command='start', description='Запустить бота 🚀'),
    ]

    class Config:
        env_prefix = 'BOT_'
        env_file = '.env'
        extra = 'ignore'


class Settings:
    
    def __init__(self):
        self.load()

    def load(self):
        self.postgres = PostgresConfig()
        self.bot = BotConfig()

    def reload(self):
        self.load()

settings = Settings()