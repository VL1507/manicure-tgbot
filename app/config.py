from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class BOT(BaseModel):
    TOKEN: str


class DB(BaseModel):
    # USER: str
    # PASSWORD: str
    # HOST: str
    # PORT: int
    # NAME: str

    URL: str


class Settings(BaseSettings):
    BOT: BOT
    DB: DB

    model_config = SettingsConfigDict(env_file="./.env", env_nested_delimiter="__")


settings = Settings()
