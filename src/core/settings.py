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
    GROQ_API_KEY: str                                                                                    
    GROQ_MODEL: str = "llama-3.3-70b-versatile"           
    GROQ_TEMPERATURE: float = 0.7                                                                        
    GROQ_TIMEOUT_SECONDS: float = 30.0


settings = Settings()
