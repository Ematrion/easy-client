from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class PackageBuilder:
    def __init__(self):
        self.created: list[Path] = []

    def paths(self) -> list[Path]:
        """Get all created paths

        Returns
        -------
        list[Path]
            All path (file or dir) created by the builder
        """
        return self.created

    def _mk_init(self, path: Path):
        self._mk_file(path / "__init__.py", "")

    def _mk_dir(self, path: Path, with_init: bool = True):
        path.mkdir(parents=True, exist_ok=True)
        self.created.append(path)
        if with_init:
            self._mk_init(path)

    def _mk_file(self, path: Path, content: str = ""):
        with open(path, "w") as f:
            f.write(content)
        self.created.append(path)


class ContentMaker:
    def __init__(self):
        self.j2env = Environment(loader=FileSystemLoader(
            Path(__file__).parent.parent / "templates"))

    def content(self, temp: str, **kwargs) -> str:
        template = self.j2env.get_template(temp)
        return template.render(**kwargs)
