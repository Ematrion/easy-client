from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class ProjectStructure:
    def __init__(self, root: Path, api_name: str, endpoints: list[str] | None = None):
        self.api_name = api_name
        self.endpoints = endpoints or []

        # usefull paths
        self.root = root
        self.api_path = self.root / self.api_name

        # jinja2 setup
        self.j2env = Environment(loader=FileSystemLoader(
            Path(__file__).parent.parent / "templates"))

        self.created: list[Path] = []

    def create(self):
        # Create the main API directory
        self._mk_dir(self.api_path)
        self._mk_config()

        # api package
        self._mk_dir(self.api_path / self.api_name)

        # fetcher (ApiClient main class)
        self._mk_fetcher()

        # validation
        self._mk_dir(self.api_path / "validation")
        for endpoint in self.endpoints:
            self._mk_file(self.api_path / "validation" /
                          f"{endpoint}_schema.py", "")

        # dataming
        self._mk_dir(self.api_path / "datamining")
        self._mk_dir(self.api_path / "datamining" / "data", False)
        self._mk_dir(self.api_path / "datamining" / "inspect")

        # tests
        self._mk_dir(self.api_path / "tests")

    # --- creating of dir/files --- #
    def _mk_init(self, path: Path):
        self._mk_file(path / "__init__.py", "")

    def _mk_dir(self, path: Path, with_init: bool = True):
        path.mkdir(parents=True, exist_ok=True)
        self.created.append(path)
        if with_init:
            self._mk_init(path)

    def _mk_file(self, path: Path, content: str):
        with open(path, "w") as f:
            f.write(content)
        self.created.append(path)

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
