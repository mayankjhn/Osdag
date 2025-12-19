import sys
import pytest
import json
from pathlib import Path

# --- CRITICAL FIX: Add 'src' to Python Path ---
# This tells Python: "Look for modules in the 'src' folder too!"
# We go up two levels from 'tests/conftest.py' to reach the root, then down into 'src'
root_path = Path(__file__).parent.parent
src_path = root_path / "src"
sys.path.insert(0, str(src_path))
# ---------------------------------------------

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
    return Path(__file__).parent.parent
