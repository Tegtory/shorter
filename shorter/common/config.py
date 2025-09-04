import string

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    HOST: str = "0.0.0.0"
    PORT: int = 9123
    DEBUG: bool = False
    DIGITS: str = string.digits + string.ascii_letters
    BLACK_LIST: list[str] = []
    URL_TEST: str = r"^https://.+"
    DB_HOST: str = "db_shorter_app"
    DB_PORT: int = 5432
    DB_NAME: str = "shorter"
    DB_USER: str = "user_shorter"
    DB_PASSWORD: str = ""

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def full_path(self) -> str:
        return self.HOST if not self.DEBUG else "http://127.0.0.1"


config = Config()
