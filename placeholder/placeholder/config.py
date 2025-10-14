"""Project settings for placeholder API."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Specs
    PLACEHOLDER_API_KEY: str | None = None
    PLACEHOLDER_API_URL: str = "https://jsonplaceholder.typicode.com"

    # Endpoints urls

    POSTS_URL: str = f"{PLACEHOLDER_API_URL}""/posts"
    COMMENTS_URL: str = f"{PLACEHOLDER_API_URL}""/comments"
    ALBUMS_URL: str = f"{PLACEHOLDER_API_URL}""/albums"
    PHOTOS_URL: str = f"{PLACEHOLDER_API_URL}""/photos"
    TODOS_URL: str = f"{PLACEHOLDER_API_URL}""/todos"
    USERS_URL: str = f"{PLACEHOLDER_API_URL}""/users"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
