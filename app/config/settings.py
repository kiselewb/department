from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # APP SETTINGS
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    APP_DOCS_URL: str
    APP_REDOC_URL: str
    ALLOWED_ORIGINS: list[str]

    # DATABASE SETTINGS
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{str(self.DB_PASS)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # LOGGER SETTINGS
    IS_FILE_LOG: bool
    IS_CONSOLE_LOG: bool
    LOG_LEVEL: str
    LOG_ROTATION: str
    LOG_COMPRESSION: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
