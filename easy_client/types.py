from typing import Any
from dataclasses import dataclass
from requests.models import Response

# typing for Fetcher class
Header = dict[str, str]
QueryParams = dict[str, Any]
ResponseData = dict[str, Any] | list[Any] | str | bytes 

# Recursive type alias for tree structure
FileTree = dict[str, "None | FileTree"]

@dataclass
class ResponseWrapper:
    status: int
    content_type: str
    data: ResponseData
    raw: Response