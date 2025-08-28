from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    HOST: str = "0.0.0.0"
    DEBUG: bool = False
    DIGITS: str = "AdeFybKopx"
    BLACK_LIST: list[str] = []
    URL_TEST: str = r"^https://.+"
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str = "shorter"
    DB_USER: str
    DB_PASSWORD: str

    def full_path(self) -> str:
        return self.HOST if not self.DEBUG else "http://127.0.0.1"


config = Config()
