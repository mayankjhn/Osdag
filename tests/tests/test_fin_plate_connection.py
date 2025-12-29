import pytest
from utils.test_helpers import run_osdag_module, assert_approximately_equal

FIN_PLATE_TEST_CASES = [
    ("FinPlateTest1", 0),
    ("FinPlateTest2", 1),
    ("FinPlateTest3", 2),
    ("FinPlateTest4", 3),
]

@pytest.mark.fin_plate
class TestFinPlateConnection:

    @pytest.mark.parametrize("filename, expected_index", FIN_PLATE_TEST_CASES)
    def test_shear_capacity(self, osdag_path, test_data_dir, expected_outputs, filename, expected_index):
        input_file = test_data_dir / "input_files" / filename
        expected = expected_outputs["fin_plate"][expected_index]
        result = run_osdag_module(osdag_path, input_file)

        assert_approximately_equal(result.get("Bolt.Capacity"), expected["shear_capacity"])

    @pytest.mark.bolt_configuration
    @pytest.mark.parametrize("filename, expected_index", [FIN_PLATE_TEST_CASES[0], FIN_PLATE_TEST_CASES[3]])
    def test_bolt_configuration(self, osdag_path, test_data_dir, expected_outputs, filename, expected_index):
        input_file = test_data_dir / "input_files" / filename
        expected = expected_outputs["fin_plate"][expected_index]
        result = run_osdag_module(osdag_path, input_file)

        assert float(result.get("Bolt.OneLine", 0)) == expected["bolt_rows"]
        assert float(result.get("Bolt.Line", 0)) == expected["bolt_columns"]
        assert float(result.get("Plate.Thickness", 0)) == expected["plate_thickness"]
