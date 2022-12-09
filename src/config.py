from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_TOKEN: str
    BOT_ENDPOINT: str
    API_KEY: str

    class Config:
        env_file = "../.env"


class Urls(BaseSettings):
    NEARBY_SEARCH_ENDPOINT: str

    class Config:
        env_file = "../.env"

settings = Settings()
urls = Urls()
