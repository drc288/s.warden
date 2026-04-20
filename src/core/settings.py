from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    APPLICATION_TITLE: str = "Warden"
    APPLICATION_DESCRIPTION: str = "Sistema de remediacion de incidentes con LLM"
    APPLICATION_VERSION: str = "0.1.0"
    APPLICATION_ENVIRONMENT: str = "development"


settings = Settings()
