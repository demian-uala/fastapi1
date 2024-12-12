from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    DB_NAME: str = "test1"
    DB_USER: str = "user1"
    DB_PASS: str = "1234"
    DB_HOST: str = 'postgresql'
    DB_PORT: int = 5432

    DATASET: str = "sandbox"
    TABLE: str = "users"
    REGION: str= "us-central1"
    PROJECT_ID: str = "uala-dataplatform-sandboxes"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
