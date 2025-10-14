from pathlib import Path

from .buildersABC import PackageBuilder


class ProjectBuilder(PackageBuilder):
    def __init__(self, root: Path, api_name: str, endpoints: list[str] | None = None):
        self.api_name = api_name
        self.endpoints = endpoints or []

        # usefull paths
        self.root = root
        self.api_path = self.root / self.api_name

        # project structure
        """
        self.tree = {
            root / api_name: {
                "tests": {},            # pytest suits
                "validation": {},       # pydantic schemas
                api_name: {        # main package
                    "fetcher.py": None,
                    "__init__.py": None,
                    "config.py": None,
                },
                "datamining": {         # api data
                    "data": {},         # collected data
                    "inspect": {},      # interactive scripts
                },
            },
        }"""

        self.tree = {
            root / api_name: {
                "tests": {},  # pytest tests for steps
                api_name: {  # main Python package
                    "__init__.py": None,
                    "config.py": None,
                    "main.py": None,  # optional pipeline entrypoint
                    "client": {
                        "__init__.py": None,
                        "fetch": {
                            "__init__.py": None,
                            "fetcher.py": None,  # BaseClass for fetching
                            "params.py": None,  # request parameters
                        },
                        "validate": {
                            **{"__init__.py": None},
                            **{f"{ep}.py": None for ep in self.endpoints},
                        },
                        "enrich": {
                            "__init__.py": None,
                        },
                        "transform": {
                            **{"__init__.py": None},
                            **{f"{ep}.py": None for ep in self.endpoints},
                        },
                        "store": {
                            "__init__.py": None,
                        },
                    },
                    "utils": {
                        "__init__.py": None,
                    },
                },
                "data": {
                    "raw": {},
                    "validated": {},
                    "transformed": {},
                    "enriched": {},
                },
                "README.md": None,
                "TODO.md": None,
            }
        }

        # tracking created paths
        self.created: list[Path] = []

    def create(self, root: Path | None = None, tree: dict | None = None):
        root = root or self.root
        tree = tree or self.tree
        for path, content in tree.items():
            if content is None:
                # it's a file
                self._mk_file(root / path, "")
            else:
                # it's a dir
                self._mk_dir(root / path)
                if content:
                    self.create(root=root / path, tree=content)

    def get_path(self, file_name: str) -> Path:
        matches = [
            path for path in self.created if path.name.endswith(file_name)]
        if not matches:
            msg = f"No created file ends with {file_name}"
            raise ValueError(msg)
        if len(matches) > 1:
            msg = f"Multiple created files end with {file_name}"
            raise ValueError(msg)
        else:
            return matches[0]  # exactly one match

    # --- creating of dir/files --- #
    '''
    def _mk_fetcher(self):
        template = self.j2env.get_template("fetcher.py.j2")
        content = template.render(api_name=self.api_name,
                                  endpoints=self.endpoints)
        self._mk_file(self.api_path / self.api_name / "fetcher.py", content)

    def _mk_config(self):
        template = self.j2env.get_template("config.py.j2")
        content = template.render(api_name=self.api_name,
                                  endpoints=self.endpoints)
        self._mk_file(self.api_path / "config.py", content)
    '''
