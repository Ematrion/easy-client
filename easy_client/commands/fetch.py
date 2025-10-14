from pathlib import Path
import os
from . import utils


def fetch(root: Path | None = None):
    print("Fetching data from API...")
    if root is None:
        root = Path(os.getcwd())

    # inputs
    api_name = utils.get_api_name()
    endpoints = utils.get_api_endpoints()

    # setups
    api_dir = root / api_name
    data_dir = root / "data" / "raw"
    fetcher_path = utils.find_path(root, "fetcher.py")

    print(api_dir)
    print(data_dir)
    print(fetcher_path)
    print(endpoints)
    fetcher_module = utils.load_module_from_path(f"{api_name.capitalize()}Fetcher",
                                                 fetcher_path,
                                                 api_dir)
    fetcher_class = getattr(fetcher_module, f"{api_name.capitalize()}Fetcher")
    fetcher = fetcher_class()
    print(fetcher)

    for endpoint in endpoints:
        method = getattr(fetcher, f"fetch_{endpoint}", None)
        if method is None:
            print(f"Warning: Method '{endpoint}' not found in fetcher.")
        else:
            data = method()
            out_path = data_dir / f"{endpoint}.json"
            with open(out_path, "w") as f:
                import json
                json.dump(data, f, indent=4)
            print(f"Saved data for endpoint '{endpoint}' to {out_path}")


if __name__ == "__main__":
    fetch()


