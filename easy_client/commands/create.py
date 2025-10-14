from pathlib import Path
from easy_client.builders.project_builder import ProjectBuilder
from easy_client.builders.buildersABC import ContentMaker
# from easy_client.types import FileTree
from .utils import tree_file_string, get_api_name, get_api_endpoints


def create(root: Path | None = None):
    print("Creating project structure...")
    if root is None:
        root = Path.cwd()

    # User interactions
    api_name = get_api_name()
    endpoints = get_api_endpoints()

    # Create project structure
    ps = ProjectBuilder(root=root,
                        api_name=api_name,
                        endpoints=endpoints)
    ps.create()

    # Display the created structure
    print("\nProject structure created:")
    print(tree_file_string(ps.tree))
    for p in ps.created:
        print(p)

    # Fill file contents
    cm = ContentMaker()
    with open(ps.get_path("fetcher.py"), "w") as f:
        f.write(cm.content("fetcher.py.j2", api_name=api_name,
                           endpoints=endpoints))
    print("\nFilled fetcher.py completed")
    with open(ps.get_path("config.py"), "w") as f:
        f.write(cm.content("config.py.j2", api_name=api_name, endpoints=endpoints))
    print("Filled config.py completed")
    with open(ps.get_path("params.py"), "w") as f:
        f.write(cm.content("params.py.j2", api_name=api_name, endpoints=endpoints))
    print("Filled params.py completed")

if __name__ == "__main__":
    create()