from easy_client.utils import DynamicLoader
from pathlib import Path


TEST_API_NAME = "placeholder"
ROOT_PATH = "."


def test_load_fetcher():
    loader = DynamicLoader(TEST_API_NAME, ROOT_PATH)
    fetcher_class = loader.load_fetcher()
    assert fetcher_class is not None


def test_load_validation_models():
    loader = DynamicLoader(TEST_API_NAME, ROOT_PATH)
    module = loader.load_models()
    print(Path(ROOT_PATH).resolve())
    assert module is not None