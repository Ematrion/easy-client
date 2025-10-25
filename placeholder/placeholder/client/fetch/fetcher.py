from easy_client import ApiFetcher
from easy_client.types import Header, ResponseData
from typing import Any

from .params import get_default_params

from placeholder.placeholder.config import settings


class PlaceholderFetcher(ApiFetcher):
    def __init__(self):
        # TODO: add PLACEHOLDER_API_URL to Settings in backend/config.py
        base_url = settings.PLACEHOLDER_API_URL
        
        # TODO: add PLACEHOLDER_API_KEY to Settings in backend/config.py
        headers = {
            "Authorization": f"Bearer {settings.PLACEHOLDER_API_KEY}",
            "Content-Type": "application/json",
        }

        # TODO: add default query params if needed
        params = {}

        # TODO: update content-type supports
        content = [
            "application/json",
            "application/xml",
            "text/html",
            "text/plain",
            "application/octet-stream",
            "image/",
            "video/"
        ]
        
        super().__init__(base_url, headers, params, content)

    def fetch_comments(self, headers: Header | None = None, **kwargs: Any) -> ResponseData:
    
        # TODO: edit params
        params = get_default_params("comments")
        params.update(kwargs)
        
        return self._request_handler(settings.COMMENTS_URL, headers=headers, params=params)


    def fetch_posts(self, headers: Header | None = None, **kwargs: Any) -> ResponseData:
    
        # TODO: edit params
        params = get_default_params("posts")
        params.update(kwargs)
        
        return self._request_handler(settings.POSTS_URL, headers=headers, params=params)


    def fetch_albums(self, headers: Header | None = None, **kwargs: Any) -> ResponseData:
    
        # TODO: edit params
        params = get_default_params("albums")
        params.update(kwargs)
        
        return self._request_handler(settings.ALBUMS_URL, headers=headers, params=params)


    def fetch_photos(self, headers: Header | None = None, **kwargs: Any) -> ResponseData:
    
        # TODO: edit params
        params = get_default_params("photos")
        params.update(kwargs)
        
        return self._request_handler(settings.PHOTOS_URL, headers=headers, params=params)


    def fetch_users(self, headers: Header | None = None, **kwargs: Any) -> ResponseData:
    
        # TODO: edit params
        params = get_default_params("users")
        params.update(kwargs)
        
        return self._request_handler(settings.USERS_URL, headers=headers, params=params)


    def fetch_todos(self, headers: Header | None = None, **kwargs: Any) -> ResponseData:
    
        # TODO: edit params
        params = get_default_params("todos")
        params.update(kwargs)
        
        return self._request_handler(settings.TODOS_URL, headers=headers, params=params)

