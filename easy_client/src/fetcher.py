from easy_client.types import Header, QueryParams, ResponseData
import requests


class ApiFetcher:
    def __init__(self, base_url: str, headers: Header):
        self.base_url = base_url
        self.headers = headers

    def _request_handler(self, url: str, headers: Header | None = None, params: QueryParams | None = None) -> ResponseData:
        if headers:
            self.headers.update(headers)
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
