import importlib
from pathlib import Path
import sys
from types import ModuleType

from easy_client import ApiFetcher

class AddToPath:
    def __init__(self, path: Path):
        self.path = str(path.resolve())
        self.inserted = False
        
    def __enter__(self):
        if self.path not in sys.path:
            sys.path.insert(0, self.path)
            self.inserted = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.inserted:
            sys.path.remove(self.path)
        
class DynamicLoader:
    def __init__(self, api_name:str, api_root:Path | str):
        if isinstance(api_root, str):
            api_root = Path(api_root)
        self.api_name = api_name
        self.api_root = api_root
        
    def load_validate_module(self) -> ModuleType:
        module_name = f"{self.api_name}.{self.api_name}.client.validate"
        with AddToPath(self.api_root):
            module = importlib.import_module(module_name)
        return module
    
    def load_fetcher(self) -> type[ApiFetcher]:
        module_name = f"{self.api_name}.{self.api_name}.client.fetch.fetcher"
        with AddToPath(self.api_root):
            module = importlib.import_module(module_name)
        fetcher_class = getattr(module, f"{self.api_name.capitalize()}Fetcher")
        return fetcher_class