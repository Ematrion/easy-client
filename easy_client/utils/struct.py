import yaml

def project_scaffold():
    with open("easy_client/structure.yaml", "r") as struct_file:
        structure = yaml.safe_load(struct_file)
    return structure

def scaffold_tree_string(structure: dict, prefix: str = "") -> str:
    lines = []
    keys = sorted(structure.keys())
    count = len(keys)
    for i, key in enumerate(keys):
        elem = None
        if key == "__meta__":
            # this is not a structural node
            continue
        elif key == "files":
            # this node contains all files of the directory
            for file in structure[key]:
                connector = "├── "
                lines.append(prefix + connector + str(file["name"]))
        else:
            # this is a directory node
            elem = key
            connector = "└── " if i == count - 1 else "├── "
            lines.append(prefix + connector + str(elem))
            extension = "    " if i == count - 1 else "│   "
            new_line = scaffold_tree_string(structure[key], prefix + extension)
            if new_line:
                lines.append(new_line)
    return "\n".join(lines)

def tree_line(prefix: str, key: str, is_last: bool) -> str:
    connector = "└── " if is_last else "├── "
    return prefix + connector + str(key)
