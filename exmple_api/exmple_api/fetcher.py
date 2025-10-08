from easy_client import ApiFetcher
from easy_client.types import Header, ResponseData # QueryParams
from typing import Any

from exmple_api.config import settings


class Exmple_apiFetcher(ApiFetcher):
    def __init__(self):
        # TODO: add EXMPLE_API_API_URL to Settings in backend/config.py
        base_url = settings.EXMPLE_API_API_URL
        
        # TODO: add EXMPLE_API_API_KEY to Settings in backend/config.py
        headers = {
            "Authorization": f"Bearer {settings.EXMPLE_API_API_KEY}",
            "Content-Type": "application/json",
        }
        super().__init__(base_url, headers)

    def fetch_endpoint1(self, id: str = ..., headers: Header | None = None, **kwargs: Any) -> ResponseData:
    
        # TODO: edit params
        params: QueryParams = {}
        params.update(kwargs)
        
        return self._request_handler(settings.ENDPOINT1_URL, headers=headers, params=params)


    def fetch_endpoint2(self, id: str = ..., headers: Header | None = None, **kwargs: Any) -> ResponseData:
    
        # TODO: edit params
        params: QueryParams = {}
        params.update(kwargs)
        
        return self._request_handler(settings.ENDPOINT2_URL, headers=headers, params=params)

