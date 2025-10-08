from pathlib import Path
from easy_client.builders.structure import ProjectStructure


# Recursive type alias for tree structure
TreeFile = dict[str, "str | TreeFile"]


def build_tree_dict(root: Path, paths: list[Path]) -> TreeFile:
    tree: TreeFile = {}
    for path in paths:
        # start from project root
        rel_path = path.relative_to(root) if path.is_absolute() else path

        # split path into tree nodes
        parts = rel_path.parts

        # start at the root of the tree / project
        current: TreeFile = tree

        # depth traversal
        for part in parts:
            # extend tree
            if part not in current:
                current[part] = {}
            # go deeper in the tree
            current = current[part]
    return tree


'''def print_tree_file(structure: dict, prefix: str = ""):
    keys = sorted(structure.keys())
    count = len(keys)
    for i, key in enumerate(keys):
        connector = "└── " if i == count - 1 else "├── "
        print(prefix + connector + key)
        extension = "    " if i == count - 1 else "│   "
        print_dict_tree(structure[key], prefix + extension)'''


def create(root: Path | None = None):
    print("Scaffolding a new API client project...")
    # Call your internal scaffolding function

    root = root or Path.cwd()
    ps = ProjectStructure(root=root,
                          api_name="exmple_api",
                          endpoints=["endpoint1", "endpoint2"])

    ps.create()

    for file in ps.created:
        print(f"Created: {file}")
    build_tree_dict(root, ps.created)
