import sys
import subprocess
import re
from pathlib import Path

def parse_osdag_output(output_text: str) -> dict:
    """
    Parses the text output from Osdag Command_line.py into a dictionary.
    """
    data = {}
    
    # Simple regex to find "Key : Value" lines
    # Adjust regex if the output format is different
    for line in output_text.splitlines():
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip()
            
            # Clean up the key/value
            # Remove symbols like || if they exist
            key = key.replace("|", "").strip()
            
            # Try to convert to float if possible
            try:
                data[key] = float(value)
            except ValueError:
                data[key] = value

    # MAPPING: Map the Osdag output keys to what our tests expect
    # This acts as a translator
    mapping = {
        # Fin Plate Mappings
        "Shear Capacity (kN)": "Bolt.Capacity",
        "Plate Thickness (mm)": "Plate.Thickness",
        "Bolt Rows": "Bolt.OneLine",
        "Bolt Columns": "Bolt.Line",
        
        # Cleat Angle Mappings
        "Shear Yielding Capacity (kN)": "Cleat.Shear",
        "Block Shear Capacity (kN)": "Cleat.BlockShear",
        "Cleat Angle Designation": "Cleat.Angle",
        "Bolt Rows (Supported Leg)": "Cleat.Spting_leg.OneLine",
        "Bolt Columns (Supported Leg)": "Cleat.Spting_leg.Line",

        # Tension Member Mappings
        "Tension Yielding Capacity (kN)": "Tension Yielding Capacity (kN)",
        "Tension Rupture Capacity (kN)": "Tension Rupture Capacity (kN)",
        "Designation": "Designation"
    }

    final_data = {}
    
    # 1. Copy raw data
    final_data.update(data)
    
    # 2. Add mapped keys so tests can find them
    for output_key, test_key in mapping.items():
        if output_key in data:
            final_data[test_key] = data[output_key]
            
    # Special Fix for Designation (remove spaces)
    if "Designation" in final_data and isinstance(final_data["Designation"], str):
         final_data["Designation"] = final_data["Designation"].replace(" ", "")

    return final_data

def run_osdag_module(osdag_path: Path, input_file_path: Path) -> dict:
    """
    Runs the Osdag Command_line.py script with a specific input file.
    """
    
    # Path to the Command_line.py script in the new repo structure
    # It lives in src/osdag/Command_line.py
    command_line_script = osdag_path / "src" / "osdag" / "Command_line.py"

    # The command to run: python src/osdag/Command_line.py --input <file>
    command = [
        sys.executable,
        str(command_line_script),
        "--input", str(input_file_path)
    ]

    # Run the command
    result = subprocess.run(
        command,
        cwd=str(osdag_path),  # Run from the root of the repo
        capture_output=True,
        text=True,
        check=False,
        env={"PYTHONPATH": str(osdag_path / "src")} # Ensure it finds the modules
    )

    if result.returncode != 0:
        print(f"Error running Osdag for input file: {input_file_path.name}")
        print(f"Stderr: {result.stderr}")
        return {}

    # Parse the output
    return parse_osdag_output(result.stdout)

def assert_approximately_equal(actual, expected, tol=0.01):
    if actual is None:
        # Don't crash, just fail the test gracefully
        raise AssertionError(f"ACTUAL value is missing. Expected: {expected}")
    try:
        val_actual = float(actual)
        val_expected = float(expected)
        if val_expected == 0:
            assert abs(val_actual) < tol
        else:
            assert abs(val_actual - val_expected) / abs(val_expected) <= tol
    except (ValueError, TypeError):
        # Fallback for strings
        assert str(actual).strip() == str(expected).strip()
