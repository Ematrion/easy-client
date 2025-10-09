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
