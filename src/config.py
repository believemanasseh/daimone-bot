from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_TOKEN: str
    BOT_ENDPOINT: str

    class Config:
        env_file = "../.env"

settings = Settings()
