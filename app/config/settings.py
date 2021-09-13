from typing import Any, Dict, List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    SERVER_NAME: str = "CORTEX"
    SERVER_HOST: AnyHttpUrl = "http://127.0.0.1:8000"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    JWT_SECRET: str = "secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP: str = "3600"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "secret"
    POSTGRES_DB: str = "test_db"
    POSTGRES_PORT: str = "5432"

    SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
