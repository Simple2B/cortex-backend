import os
from typing import Any, Dict, List, Union, Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    SERVER_NAME: str = "CORTEX"
    SERVER_HOST: AnyHttpUrl = "http://127.0.0.1:8000"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    JWT_SECRET: str = "secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP: str = "3600"
    SK_TEST: str = "sk_secret"
    # PK_TEST: str = "pk_secret"
    # CORTEX_KEY: str = "rk_secret"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "secret"
    POSTGRES_DB: str = "test_db"
    POSTGRES_PORT: str = "5432"
    LOCAL_DB_PORT: str = "11"
    LOCAL_DB_SERVER: str = "127.0.0.1"
    FLASK_ENV: str = "production"
    SQLALCHEMY_DATABASE_URL: str = None
    PK_TEST: str = "pk_secret"
    CORTEX_KEY: str = "rk_secret"

    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if os.environ.get("TESTING", None):
            from admin.config import TestingConfig

            return TestingConfig.SQLALCHEMY_DATABASE_URI
        if isinstance(v, str):
            return v
        env = os.environ.get("FLASK_ENV", "develop")
        host = (
            values.get("POSTGRES_SERVER")
            if env == "production"
            else values.get("LOCAL_DB_SERVER")
        )
        port = (
            values.get("POSTGRES_PORT")
            if env == "production"
            else values.get("LOCAL_DB_PORT")
        )
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            PK_TEST=values.get("PK_TEST"),
            CORTEX_KEY=values.get("CORTEX_KEY"),
            host=host,
            port=port,
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
