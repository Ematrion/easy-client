from pathlib import Path
# from backend import config

from jinja2 import Environment, FileSystemLoader


# settings = config.get_settings()


class ApiProjectBuilder:
    def __init__(self, api_name: str, endpoints: list[str] | None = None, root: Path | None = None):
        # api specifics
        self.api_name = api_name
        self.endpoints = endpoints or []

        # paths
        self.root = root or Path.cwd()
        print('root', self.root)
        self.project_path = self.root / api_name
        print('project', self.project_path)
        self.api_path = self.project_path / "api"
        print('client', self.api_path)
        self.dataminig_dir = self.project_path / "datamining"
        self.data = self.dataminig_dir / "data"
        self.inspectors_dir = self.dataminig_dir / "inspect"
        self.tests_dir = self.project_path / "tests"

        # jinja2 setup
        self.j2env = Environment(loader=FileSystemLoader("templates/"))

        # tracking created files and dirs
        self.created: list[Path] = []

    def create_source_structure(self):
        # sources folder
        self._mk_dir(self.api_path)
        self._mk_dir(self.dataminig_dir)

        # __init__.py files
        self._mk_file(self.api_path / "__init__.py",
                      f"# Package to collect data from {self.api_name} api\n")
        self._mk_file(self.dataminig_dir / "__init__.py",
                      f"# {self.api_name} v1 package\n")

    def _mk_dir(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        self.created.append(path)

    def _mk_file(self, path: Path, content: str):
        with open(path, "w") as f:
            f.write(content)
        self.created.append(path)

    def _mk_client(self):
        # template = self.j2env.get_template("api_client.py.j2")
        # content = template.render(
        #    api_name=self.api_name,
        #    endpoints=self.endpoints
        # )
        # path = self.v1_path / "client.py"
        # self._mk_file(path, content)
        # self.created.append(path)
        ...

        # --- better code structure --- #
    def create_ingestion_structure(self):
        ...

    def create_validation_structure(self):
        ...

    def create_filtering_structure(self):
        ...

    def create_enrichement_structure(self):
        ...

    def create_normalization_structure(self):
        ...

    def create_persistence_structure(self):
        ...

    def create_pipeline_structure(self):
        ...

    def create_documentation(self):
        ...
