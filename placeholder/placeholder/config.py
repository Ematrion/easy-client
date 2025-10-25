"""Project settings for placeholder API."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #API Specs
    PLACEHOLDER_API_KEY: str | None = None
    PLACEHOLDER_API_URL: str = "https://jsonplaceholder.typicode.com"

    # Endpoints urls
    
    COMMENTS_URL: str = f"{ PLACEHOLDER_API_URL }/comments"
    POSTS_URL: str = f"{ PLACEHOLDER_API_URL }/posts"
    ALBUMS_URL: str = f"{ PLACEHOLDER_API_URL }/albums"
    PHOTOS_URL: str = f"{ PLACEHOLDER_API_URL }/photos"
    USERS_URL: str = f"{ PLACEHOLDER_API_URL }/users"
    TODOS_URL: str = f"{ PLACEHOLDER_API_URL }/todos"


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()