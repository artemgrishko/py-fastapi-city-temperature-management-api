from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI city temperature api"

    DATABASE_URL: str | None = "sqlite:///./city-temperature.db"

    class Config:
        case_sensitive = True


settings = Settings()
