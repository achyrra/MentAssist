import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    APP_DB_USER: str = os.getenv("APP_DB_USER", "")
    APP_DB_PASSWORD: str = os.getenv("APP_DB_PASSWORD", "")
    APP_DB_HOST: str = os.getenv("APP_DB_HOST", "localhost")
    APP_DB_PORT: str = os.getenv("APP_DB_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")

    def validate(self):
        if not self.DATABASE_URL:
            raise RuntimeError("DATABASE_URL not set")


settings = Settings()
settings.validate()