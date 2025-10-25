from pathlib import Path
import os
import easy_client.utils as utils
from easy_client.utils import DynamicLoader

def fetch(root: Path | None = None):
    print("Fetching data from API...")
    if root is None:
        root = Path(os.getcwd())

    # inputs
    api_name = utils.get_api_name()
    endpoints = utils.get_api_endpoints()

    # setups
    data_dir = root / api_name /"data" / "raw"
    fetcher_class = DynamicLoader(api_name, root).load_fetcher()
    fetcher = fetcher_class() # type: ignore -- use protcols to fix this
    
    print(data_dir)
    print(endpoints)
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


