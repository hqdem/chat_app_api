from typing import Dict, Any

from pydantic import BaseSettings, validator, PostgresDsn


class Settings(BaseSettings):
    API_PREFIX: str = 'api/v1'
    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        env_file = '.env'


settings = Settings()
