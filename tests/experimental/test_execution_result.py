import unittest
from requiem_testing.experimental.execution import SimpleProgramExecutionResult


def _make_result(all_output_data: bytes, exit_code: int = 1) -> SimpleProgramExecutionResult:
    return SimpleProgramExecutionResult(all_output_data, exit_code)


class TestSimpleProgramExecutionResultLineCounting(unittest.TestCase):
    def test_should_return_0_when_the_output_from_the_program_is_empty(self):
        result = _make_result(b"")
        self.assertEqual(0, result.count_lines())

    def test_should_return_1_when_there_is_only_one_line_in_output_with_just_lf(self):
        result = _make_result(b"abc\n")
        self.assertEqual(1, result.count_lines())

    def test_should_return_2_when_there_are_two_lines_in_output_separated_by_just_lf(self):
        result = _make_result(b"abc\ndef\n")
        self.assertEqual(2, result.count_lines())