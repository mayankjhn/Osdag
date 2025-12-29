import sys
from pathlib import Path
import logging
import io
import contextlib


current_dir = Path(__file__).parent

# Repo Root: Osdag/
repo_root = current_dir.parent.parent

# Source Code: Osdag/src
osdag_src = repo_root / "src"

# Add src to sys.path so we can import 'osdag'
if str(osdag_src) not in sys.path:
    sys.path.insert(0, str(osdag_src))

# Now this import should work if cli.py exists in src/osdag/cli.py
try:
    from osdag.cli import run_module
except ImportError:
    # Fallback if the folder structure is slightly different (e.g. src/cli.py vs src/osdag/cli.py)
    # Check if cli.py is directly in src or src/osdag
    print(f"DEBUG: Could not import osdag.cli. looking in {osdag_src}")
    raise

def run_osdag_module(osdag_path: Path, input_file_path: Path) -> dict:
    captured = io.StringIO()
    # Suppress logging
    osdag_logger = logging.getLogger("Osdag")
    prev_level = getattr(osdag_logger, "level", None)
    if osdag_logger:
        osdag_logger.setLevel(logging.WARNING)

    # Run the module using the internal function (Fast!)
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        try:
            result = run_module(
                input_path=str(input_file_path.absolute()),
                op_type="print_result"
            )
        except Exception as e:
            print(f"CRITICAL ERROR running Osdag: {e}")
            return {}

    if prev_level is not None:
        osdag_logger.setLevel(prev_level)

    if not result.get("success", True):
        return {}

    data = result.get("data", {}) or {}
    out = dict(data)

    # --- HELPER FUNCTIONS ---
    def normalize_designation(val):
        if not val: return val
        if isinstance(val, (list, tuple)): val = val[0]
        return str(val).replace(" ", "")

    # --- MAPPING (Translates Osdag output to Test Expectations) ---
    mapping = {
        # Fin Plate
        "section_size.designation": "Designation",
        "Plate.TensionYield": "Tension Yielding Capacity (kN)", 
        "Plate.TensionRupture": "Tension Rupture Capacity (kN)",
        "Plate.Shear": "Shear Capacity (kN)",
        "Bolt.Shear": "Bolt.Capacity",  # Verify this key name in your JSON!
        "Bolt.Capacity": "Bolt.Capacity",
        
        # Cleat Angle
        "Cleat.Angle": "Cleat.Angle",
        "Cleat.Shear": "Cleat.Shear",
        "Cleat.BlockShear": "Cleat.BlockShear",
        
        # Tension
        "Member.designation": "Designation",
        "Member.tension_yielding": "Tension Yielding Capacity (kN)",
        "Member.tension_capacity": "Tension Capacity (kN)",
        "Member.tension_rupture": "Tension Rupture Capacity (kN)",
    }

    for src, dst in mapping.items():
        if src in data:
            out[dst] = data[src]

    if "Designation" in out and out["Designation"]:
        out["Designation"] = normalize_designation(out["Designation"])

    # Bolt Row/Col Logic
    one_line = data.get("Bolt.OneLine") or data.get("Cleat.Spting_leg.OneLine")
    line = data.get("Bolt.Line") or data.get("Cleat.Spting_leg.Line")
    
    # Try to map them to "Bolt.OneLine" / "Bolt.Line" if your tests expect that
    if one_line: out["Bolt.OneLine"] = one_line
    if line: out["Bolt.Line"] = line

    return out

def assert_approximately_equal(actual, expected, tol=0.01):
    if actual is None:
        raise AssertionError(f"ACTUAL value is missing. Expected: {expected}")
    try:
        val_actual = float(actual)
        val_expected = float(expected)
        if val_expected == 0:
            assert abs(val_actual) < tol
        else:
            assert abs(val_actual - val_expected) / abs(val_expected) <= tol
    except (ValueError, TypeError):
        assert str(actual).strip() == str(expected).strip()
