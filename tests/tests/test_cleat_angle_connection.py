import pytest
from utils.test_helpers import run_osdag_module, assert_approximately_equal

CLEAT_ANGLE_TEST_CASES = [
    ("CleatAngleTest1.osi", 0),
    ("CleatAngleTest2.osi", 1),
    ("CleatAngleTest3.osi", 2),
    ("CleatAngleTest4.osi", 3),
]

@pytest.mark.cleat_angle
class TestCleatAngleConnection:

    @pytest.mark.parametrize("filename, expected_index", CLEAT_ANGLE_TEST_CASES)
    def test_shear_capacity(self, osdag_path, test_data_dir, expected_outputs, filename, expected_index):
        input_file = test_data_dir / "input_files" / filename
        expected = expected_outputs["cleat_angle"][expected_index]
        result = run_osdag_module(osdag_path, input_file)

        assert_approximately_equal(result.get("Cleat.Shear"), expected["shear_yielding_capacity"])
        assert_approximately_equal(result.get("Cleat.BlockShear"), expected["block_shear_capacity"])

    @pytest.mark.designation
    @pytest.mark.parametrize("filename, expected_index", [CLEAT_ANGLE_TEST_CASES[0], CLEAT_ANGLE_TEST_CASES[1]])
    def test_designation(self, osdag_path, test_data_dir, expected_outputs, filename, expected_index):
        input_file = test_data_dir / "input_files" / filename
        expected = expected_outputs["cleat_angle"][expected_index]
        result = run_osdag_module(osdag_path, input_file)

        actual = result.get("Cleat.Angle", "").replace(" ", "")
        expected_designation = str(expected["designation"]).replace(" ", "")
        assert actual == expected_designation

    @pytest.mark.bolt_configuration
    @pytest.mark.parametrize("filename, expected_index", [CLEAT_ANGLE_TEST_CASES[2], CLEAT_ANGLE_TEST_CASES[3]])
    def test_bolt_configuration(self, osdag_path, test_data_dir, expected_outputs, filename, expected_index):
        input_file = test_data_dir / "input_files" / filename
        expected = expected_outputs["cleat_angle"][expected_index]
        result = run_osdag_module(osdag_path, input_file)

        assert float(result.get("Cleat.Spting_leg.OneLine", 0)) == expected["bolt_rows_supported_leg"]
        assert float(result.get("Cleat.Spting_leg.Line", 0)) == expected["bolt_columns_supported_leg"]
