import pytest
import json
from pathlib import Path

@pytest.fixture(scope="session")
def test_data_dir():
    return Path(__file__).parent / "test_data"

@pytest.fixture(scope="session")
def expected_outputs(test_data_dir):
    json_path = test_data_dir / "expected_outputs.json"
    with open(json_path, 'r') as f:
        return json.load(f)

@pytest.fixture(scope="session")
def osdag_path():
    return Path(__file__).parent.parent / "osdag-main"
