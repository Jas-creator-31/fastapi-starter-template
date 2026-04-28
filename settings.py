from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    
)
from pydantic import (
    Field,
    SecretStr
)

class Settings(BaseSettings):
    self_url: str = Field(
        validation_alias="SELF_URL"
    )

    db_driver: str = Field(
        validation_alias="DB_DRIVER"
    )
    db_username: str = Field(
        validation_alias="DB_USERNAME"
    )
    db_secret_key: SecretStr = Field(
        validation_alias="DB_PASSWORD"
    )
    db_host: str = Field(
        validation_alias="DB_HOST"
    )
    db_port: int = Field(
        validation_alias="DB_PORT"
    )
    db_name: str = Field(
        validation_alias="DB_NAME"
    )

    # Redis
    redis_host: str = Field(
        validation_alias="REDIS_HOST"
    )
    redis_port: int = Field(
        validation_alias="REDIS_PORT"
    )
    redis_db: int = Field(
        validation_alias="REDIS_DB"
    )

    # JWT and others
    jwt_algorithm: str = "HS256"
    jwt_secret: SecretStr = Field(
        validation_alias="JWT_SECRET_KEY"
    )
    csrf_key: SecretStr = Field(
        validation_alias="CSRF_SECRET_KEY"
    )

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        # extra="forbid",  # Raises error if extra vars are in .env
    )

settings = Settings() # type: ignore
