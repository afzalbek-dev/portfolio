import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Developer Portfolio API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./portfolio.db")

    # Telegram Bot & Admin Configuration
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "8634355926:AAFx28R6F8HUXQhqJYI2WnSd9BYVcxGp4rA")
    TELEGRAM_ADMIN_ID: str = os.getenv("TELEGRAM_ADMIN_ID", "7196940979")
    TELEGRAM_ADMIN_IDS_RAW: str = os.getenv("TELEGRAM_ADMIN_IDS", "7196940979")

    @property
    def admin_ids(self) -> list[int]:
        ids = []
        raw_list = self.TELEGRAM_ADMIN_IDS_RAW.split(",") + [self.TELEGRAM_ADMIN_ID]
        for item in raw_list:
            cleaned = item.strip()
            if cleaned.isdigit():
                ids.append(int(cleaned))
        return list(set(ids))

    # Media Upload Directory
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "*"
    ]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
