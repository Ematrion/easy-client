from easy_client.types import Header, QueryParams, ResponseData, ResponseWrapper
import requests
from requests.models import Response
import json
#from typing import Callable, Any


def _extract_json(response: Response) -> ResponseData:
    return response.json()
    
def _extract_xml(response: Response) -> ResponseData:
    ...
    
def _extract_html(response: Response) -> ResponseData:
    ...

def _extract_text(response: Response) -> ResponseData:
    return response.text

def _extract_bytes(response: Response) -> ResponseData:
    return response.content

def _extract_image(response: Response) -> ResponseData:
    return response.content

def _extract_video(response: Response) -> ResponseData:
    ...

EXTRACTORS = {
                "application/json": _extract_json,
                "application/xml": _extract_xml,
                "text/html": _extract_html,
                "text/plain": _extract_text,
                "application/octet-stream": _extract_bytes,
                "image/": _extract_image,
                "video/": _extract_video,
            }

class ApiFetcher:
    def __init__(self, base_url: str, headers: Header, params: QueryParams, contents: list[str]):
        self.base_url = base_url
        self.headers = headers
        self.params = params
        self.extractors = {content: EXTRACTORS[content] for content in contents}

    def _request_handler(self, url: str, headers: Header | None = None, params: QueryParams | None = None) -> ResponseData:
        # merge default headers/params with priority for passed ones
        if headers:
            headers = {**self.headers, **headers}
        if params:
            params = {**self.params, **params}

        response = requests.get(url, headers=headers, params=params)
        resp = self._response_handler(response)
        return resp.data

    def _response_handler(self, response: Response) -> ResponseWrapper:
        status = response.status_code
        content_type = response.headers.get("Content-Type", "").split(";")[0]
        data = self.extractors[content_type](response)
        return ResponseWrapper(status=status, content_type=content_type, data=data, raw=response)
