# загрузка настроек из .env
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    admin_ids: str = ""
    database_url: str = "sqlite+aiosqlite:///bot.db"
    menu_url: str = "https://debassus.ru/vrn/menu/menudbvena.pdf"

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env")
    main
