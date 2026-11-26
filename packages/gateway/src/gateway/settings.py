from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = Field(default=5432, ge=1, le=65535)
    password: SecretStr = Field(min_length=12)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="GATEWAY_", env_nested_delimiter="__", hide_input_in_errors=True
    )

    debug: bool = False
    db: DatabaseSettings


def load_settings() -> Settings:
    # db is filled from GATEWAY_DB__* environment variables at runtime
    return Settings()  # pyright: ignore[reportCallIssue]
