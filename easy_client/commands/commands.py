from pathlib import Path
from easy_client.builders.project_builder import ProjectBuilder
# from easy_client.types import FileTree


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


def create(root: Path | None = None):
    print("Scaffolding a new API client project...")
    # Call your internal scaffolding function

    root = root or Path.cwd()
    ps = ProjectBuilder(root=root,
                        api_name="exmple_api",
                        endpoints=["endpoint1", "endpoint2"])

    ps.create()

    for file in ps.created:
        print(f"Created: {file}")
    print(tree_file_string(ps.tree))
