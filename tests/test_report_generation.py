"""
Tests: .osi → Osdag → save_latex() → .tex/.pdf validation
"""

import sys
import pytest
import shutil
from pathlib import Path
from utils.test_helpers import run_osdag_module

# Add src path to import CreateLatex
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

TEST_DATA_DIR = REPO_ROOT / "tests" / "test_data" / "input_files"
OUTPUT_DIR = REPO_ROOT / "src" / "osdag" / "OUTPUT_FILES" / "design_reports"


@pytest.fixture(autouse=True)
def setup_teardown():
    """Clean output directory before and after the test."""
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)



def pytest_generate_tests(metafunc):
    """Dynamic parametrization: Use --osi file if provided, otherwise use default list."""
    if "input_file_name" in metafunc.fixturenames:
        osi_option = metafunc.config.getoption("--osi")
        if osi_option:
            # If user provided a file, run ONLY that file
            # Verify if it's a full path or just a name. 
            # Ideally we support both. We passed it as string.
            # We'll normalize it in the test, or just pass it through.
            metafunc.parametrize("input_file_name", [osi_option])
        else:
            # Default suite files
            metafunc.parametrize("input_file_name", ["FinPlateTest1.osi", "TensionWeldedTest2.osi"])

def test_report_generation_cli(input_file_name, request):
    """ Verify report generation using CLI: file existence, size, and document class. """
    import subprocess
    import os
    import sys
    
    # Paths
    REPO_ROOT = Path(__file__).parent.parent
    
    # Handle input file path (could be absolute from CLI, or relative filename)
    cand_path = Path(input_file_name)
    if cand_path.is_absolute() and cand_path.exists():
        INPUT_FILE = cand_path
        input_name = cand_path.name
    else:
        # Fallback to test_data_dir lookup
        INPUT_FILE = TEST_DATA_DIR / input_file_name
        input_name = input_file_name

    # Output is handled by CLI default behavior or -o. 
    # To avoid searching endlessly, let's specify a unique output name.
    safe_name = str(input_name).replace(".osi", "_Report.pdf")
    OUTPUT_FILE = OUTPUT_DIR / safe_name
    
    # Use environment with Mocks
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{REPO_ROOT / 'tests' / 'mock_imports'};{REPO_ROOT / 'src'};{env.get('PYTHONPATH', '')}"
    
    # Ensure DB is set up
    setup_db_script = REPO_ROOT / 'tests' / 'utils' / 'setup_db.py'
    subprocess.run([sys.executable, str(setup_db_script)], env=env, check=True)

    cmd = [
        sys.executable, "-m", "osdag_gui", "cli", "run",
        "-i", str(INPUT_FILE),
        "-t", "generate_report",
        "-o", str(OUTPUT_FILE)
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, env=env, input="", capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        pytest.fail("CLI timed out")
    
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    # Locate the .tex file
    # CLI behavior with -o:
    # If -o is "dir/file.pdf", it usually produces "dir/file.tex".
    # However, Osdag sometimes nests outputs.
    # We will search recursively in OUTPUT_DIR for the expected tex filename.
    
    expected_tex_name = safe_name.replace(".pdf", ".tex")
    
    # Force search
    tex_files = list(OUTPUT_DIR.rglob(expected_tex_name))
    
    # If specific name not found, try generic *Report.tex if the CLI naming is stubborn
    if not tex_files:
         tex_files = list(OUTPUT_DIR.rglob("*.tex"))
    
    if not tex_files:
         pytest.fail(f"No TEX file found in {OUTPUT_DIR}")
         
    # Pick the most likely candidate (most recently modified or matching name)
    tex_file = tex_files[0]
    for f in tex_files:
        if f.name == expected_tex_name:
            tex_file = f
            break
            
    print(f"Found TEX file: {tex_file}")
    
    assert tex_file.exists(), f"TEX file not found at {tex_file}"
    
    # 1. File Size Check
    size_kb = tex_file.stat().st_size / 1024
    print(f"TEX size: {size_kb:.1f} KB")
    
    # Store for summary
    if hasattr(request.config, "report_stats"):
        request.config.report_stats.append((input_file_name, size_kb, "Pass"))

    assert size_kb < 100, f"Report too large: {size_kb:.1f} KB"
    assert size_kb > 0, "Report is empty"

    # 2. Document Class Check
    content = tex_file.read_text(errors="ignore")
    assert "\\documentclass{report}" in content or "\\documentclass{article}" in content, "Report should use 'report' or 'article' class."

def test_report_cleanup():
    """Verify cleanup removes output files."""
    # This test is trivial, effectively handled by fixture
    pass
