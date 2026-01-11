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


def test_finplate_report_end_to_end():
    """.osi → Osdag → save_latex → validate output"""

    # 1. Run Osdag design
    input_file = TEST_DATA_DIR / "FinPlateTest1.osi"
    print("Running Osdag FinPlate...")
    results = run_osdag_module(REPO_ROOT, input_file)

    # Pull fields if present, otherwise fall back to empty defaults
    uiObj = results.get("uiObj", {})
    Design_Check = results.get("Design_Check", [])
    reportsummary = results.get("reportsummary", {})
    Disp_2d_image = results.get("Disp_2d_image", [])
    Disp_3d_image = results.get("Disp_3d_image", "")
    module = results.get("module", "")

    # reportsummary must be present or save_latex cannot run
    assert reportsummary, "reportsummary missing — run returned no usable metadata"

    # 2. Call CreateLatex.save_latex
    from osdag.design_report.reportGenerator_latex import CreateLatex
    latex = CreateLatex()

    filename = "FinPlateTestReport"
    rel_path = str(OUTPUT_DIR) + "/"

    print("Calling CreateLatex.save_latex()...")
    ok = latex.save_latex(
        uiObj,
        Design_Check,
        reportsummary,
        filename,
        rel_path,
        Disp_2d_image,
        Disp_3d_image,
        module
    )

    # 3. Validate expected files
    tex_file = OUTPUT_DIR / f"{filename}.tex"
    pdf_file = OUTPUT_DIR / f"{filename}.pdf"

    print(f"Expected TEX: {tex_file}")
    print(f"Expected PDF: {pdf_file}")

    assert tex_file.exists(), "TEX report was not generated"
    assert pdf_file.exists(), "PDF report was not generated"

    size_kb = tex_file.stat().st_size / 1024
    print(f"TEX size: {size_kb:.1f} KB")
    assert size_kb < 2000, f"Report too large: {size_kb:.1f} KB"

    content = tex_file.read_text(errors="ignore")
    assert "\\documentclass" in content, "Missing documentclass in generated TEX"

    print("FinPlate report created successfully.")


def test_report_cleanup():
    """Verify cleanup removes output files."""
    assert not list(OUTPUT_DIR.glob("*.*")), "Leftover files found"
