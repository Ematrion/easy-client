from easy_client import ApiFetcher
from easy_client.types import Header, ResponseData
from typing import Any

from .params import get_default_params

from test_nw.test_nw.config import settings


class Test_nwFetcher(ApiFetcher):
    def __init__(self):
        # TODO: add TEST_NW_API_URL to Settings in backend/config.py
        base_url = settings.TEST_NW_API_URL
        
        # TODO: add TEST_NW_API_KEY to Settings in backend/config.py
        headers = {
            "Authorization": f"Bearer {settings.TEST_NW_API_KEY}",
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
