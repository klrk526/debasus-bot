#загрузка настроек из .env: токен бота, ID админо, URL базы данных
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    admin_ids: str = ""
    database_url: str = "sqlite+aiosqlite:///bot.db"

    class Config:
        env_file = ".env"


settings = Settings()