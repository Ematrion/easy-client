"""Project settings for test_nw API."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #API Specs
    TEST_NW_API_KEY: str | None = None
    TEST_NW_API_URL: str = ""

    # Endpoints urls
    


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()