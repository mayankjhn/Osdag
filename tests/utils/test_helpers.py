import sys
from pathlib import Path
import logging
import io
import contextlib

# Make osdag src importable
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
osdag_src = project_root / "osdag-main" / "src"

if str(osdag_src) not in sys.path:
    sys.path.insert(0, str(osdag_src))

from osdag.cli import run_module


def run_osdag_module(osdag_path: Path, input_file_path: Path) -> dict:
    captured = io.StringIO()
    osdag_logger = logging.getLogger("Osdag")
    prev_level = getattr(osdag_logger, "level", None)
    if osdag_logger:
        osdag_logger.setLevel(logging.WARNING)

    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        result = run_module(
            input_path=str(input_file_path.absolute()),
            op_type="print_result"
        )

    if prev_level is not None:
        osdag_logger.setLevel(prev_level)

    if not result.get("success", True):
        return {}

    data = result.get("data", {}) or {}
    out = dict(data)

    def normalize_designation(val):
        if not val:
            return val
        if isinstance(val, (list, tuple)):
            val = val[0]
        return str(val).replace(" ", "")

    mapping = {
        "section_size.designation": "Designation",
        "section.designation": "Designation",
        "Member.designation": "Designation",
        "Cleat.Angle": "Designation",
        "Member.tension_yielding": "Tension Yielding Capacity (kN)",
        "Member.tension_capacity": "Tension Capacity (kN)",
        "Member.tension_rupture": "Tension Rupture Capacity (kN)",
        "Plate.TensionYield": "Tension Yielding Capacity (kN)",
        "Plate.TensionRupture": "Tension Rupture Capacity (kN)",
        "Plate.Shear": "Shear Capacity (kN)",
        "Bolt.Shear": "Shear Yielding Capacity (kN)",
        "Bolt.Capacity": "Shear Yielding Capacity (kN)",
        "Cleat.Shear": "Shear Yielding Capacity (kN)",
    }
    for src, dst in mapping.items():
        if src in data and dst not in out:
            out[dst] = data[src]

    if "Designation" in out and out["Designation"]:
        out["Designation"] = normalize_designation(out["Designation"])

    one_line = data.get("Bolt.OneLine") or data.get("Cleat.Spting_leg.OneLine")
    line = data.get("Bolt.Line") or data.get("Cleat.Spting_leg.Line")
    try:
        if one_line is not None:
            out["Bolt-rows"] = int(float(one_line))
        if line is not None:
            out["Bolt-columns"] = int(float(line))
    except Exception:
        if one_line is not None and "Bolt-rows" not in out:
            out["Bolt-rows"] = one_line
        if line is not None and "Bolt-columns" not in out:
            out["Bolt-columns"] = line

    if "Plate thickness (mm)" not in out and "Plate.Thickness" in data:
        try:
            out["Plate thickness (mm)"] = float(data["Plate.Thickness"])
        except Exception:
            out["Plate thickness (mm)"] = data["Plate.Thickness"]

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
