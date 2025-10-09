from typing import Any


Header = dict[str, str]
QueryParams = dict[str, Any]
ResponseData = dict[str, Any] | list[Any] | str | None

# Recursive type alias for tree structure
FileTree = dict[str, "None | FileTree"]
