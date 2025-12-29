import pytest
from utils.test_helpers import run_osdag_module, assert_approximately_equal

TENSION_MEMBER_TEST_CASES = [
    ("TensionWeldedTest1", 0),
    ("TensionWeldedTest2", 1),
    ("TensionWeldedTest3", 2),
    ("TensionWeldedTest4", 3),
]

@pytest.mark.tension_welded
class TestTensionMemberWelded:

    @pytest.mark.parametrize("filename, expected_index", TENSION_MEMBER_TEST_CASES)
    def test_capacity(self, osdag_path, test_data_dir, expected_outputs, filename, expected_index):
        input_file = test_data_dir / "input_files" / filename
        expected = expected_outputs["tension_welded"][expected_index]
        result = run_osdag_module(osdag_path, input_file)

        assert_approximately_equal(result["Tension Yielding Capacity (kN)"], expected["tension_yielding_capacity"])
        assert_approximately_equal(result["Tension Rupture Capacity (kN)"], expected["tension_rupture_capacity"])

    @pytest.mark.designation
    @pytest.mark.parametrize("filename, expected_index", [TENSION_MEMBER_TEST_CASES[0], TENSION_MEMBER_TEST_CASES[3]])
    def test_designation(self, osdag_path, test_data_dir, expected_outputs, filename, expected_index):
        input_file = test_data_dir / "input_files" / filename
        expected = expected_outputs["tension_welded"][expected_index]
        result = run_osdag_module(osdag_path, input_file)

        assert result["Designation"] == expected["designation"]
