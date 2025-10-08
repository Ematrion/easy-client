from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Project settings for exmple_api API."""
    EXMPLE_API_API_KEY: str = ""
    EXMPLE_API_API_URL: str = ""

    ENDPOINT1_URL: str = ""

    ENDPOINT2_URL: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
