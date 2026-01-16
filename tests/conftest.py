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

@pytest.fixture
def osdag_path():
    """Return the Osdag source directory"""
    return Path(__file__).parent.parent

def pytest_addoption(parser):
    """Add CLI option to specify a custom .osi file for testing report generation."""
    parser.addoption("--osi", action="store", default=None, help="Path to specific .osi file to test report generation")

def pytest_configure(config):
    """Register a custom marker or stash for report stats."""
    # We will use a global list in config to store report stats
    config.report_stats = []

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print the report size summary table at the end of the run."""
    stats = getattr(config, "report_stats", [])
    if not stats:
        return
    
    terminalreporter.section("Generated Report Statistics")
    terminalreporter.write_line(f"{'Report Name':<40} | {'Size (KB)':<10} | {'Status':<10}")
    terminalreporter.write_line("-" * 65)
    
    for name, size, status in stats:
        terminalreporter.write_line(f"{name:<40} | {size:<10.2f} | {status:<10}")

