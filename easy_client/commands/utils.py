from types import ModuleType
from pathlib import Path
import importlib
import sys


def get_api_name() -> str:
    api_name = input("Enter an API name (e.g., 'my_api'): ").strip().lower()
    if not api_name.isidentifier():
        raise ValueError(
            "Invalid API name. Must be a valid Python identifier.")
    return api_name


def get_api_endpoints() -> list[str]:
    endpoints_input = input(
        "Enter endpoints (comma-separated, e.g., 'users,posts,comments'): ").strip()
    endpoints = [ep.strip() for ep in endpoints_input.split(",") if ep.strip()]
    return endpoints


def tree_file_string(structure: dict, prefix: str = "") -> str:
    lines = []
    keys = sorted(structure.keys())
    count = len(keys)
    for i, key in enumerate(keys):
        connector = "└── " if i == count - 1 else "├── "
        lines.append(prefix + connector + str(key))
        extension = "    " if i == count - 1 else "│   "
        if structure[key]:  # could be None or {}
            lines.append(tree_file_string(structure[key], prefix + extension))
    return "\n".join(lines)


def find_path(cwd: Path, target: str):
    candidates = list(cwd.rglob(target))
    if len(candidates) != 1:
        msg = f"Could not identify {target}."
        msg += f"\nFound: {candidates}"
        msg += "\nExpected exactly one"
        raise RuntimeError(msg)
    else:
        return candidates[0]


def path_to_module_string(file_path: Path, api_root: Path) -> str:
    rel_path = file_path.relative_to(api_root).with_suffix("")
    return ".".join(rel_path.parts)


def load_module_from_path(module_name: str, file_path: Path, api_root: Path) -> ModuleType:
    sys.path.insert(0, str(api_root))

    print(module_name, file_path, api_root, '\n')
    module_name = path_to_module_string(file_path, api_root)
    module = importlib.import_module(module_name)

    sys.path.pop(0)

    return module
