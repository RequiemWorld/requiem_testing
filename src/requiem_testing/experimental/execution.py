import re
import subprocess
from requiem_testing.experimental.envparse import StrictEnvironmentParser


class SimpleProgramExecutionResult:
    """
    A simple result of the programs execution which contains the exit code, and data that was output
    to stdout and stderr combined, in the execution to get this result, stderr would be redirected to stdout.
    """
    def __init__(self, all_output_data: bytes, exit_code: int):
        self._all_output_data = all_output_data
        self._exit_code = exit_code

    def _has_line(self, line_without_separator: str) -> bool:
        for line_data in self.read_lines():
            if line_data.decode() == line_without_separator:
                return True
        return False

    @property
    def exit_code(self):
        return self._exit_code

    def read_lines(self) -> list[bytes]:
        # the idea is that this can be made cross-platform by rewriting \r\n to just \n and then
        # reading line by line that way, assuming the process is one that is going to print out lines.
        normalized_output_data = re.sub(b"\r\n", b"\n", self._all_output_data)
        return [line for line in  normalized_output_data.split(b"\n") if line != b""]

    def count_lines(self) -> int:
        return len(self.read_lines())

    def assert_has_line(self, line_without_separator: str) -> None:
        found_matching_line = self._has_line(line_without_separator)
        assert found_matching_line, f"no line matching {line_without_separator} was found"

    def assert_exact_line_output(self, lines_without_separators: list[str]):
        for line in lines_without_separators:
            self.assert_has_line(line)

    def assert_has_exact_number_of_lines(self, number: int):
        number_of_lines = self.count_lines()
        assert number_of_lines == number, f"has {number_of_lines} and not {number} ... {self.read_lines()}"

    def assert_has_only_one_line(self) -> None:
        self.assert_has_exact_number_of_lines(1)

    def assert_does_not_have_line(self, line_without_separator: str):
        assert not self._has_line(line_without_separator), f"line was found in {self._all_output_data}"


class SimpleProgramExecutor:
    """
    Executes a program and continually reads stderr and stdout until it is finished. stderr is redirected
    to stdout and the result will have the combination of both in one. An unlimited amount can be captured.
    """
    def execute_program(self, command: list[str], environment: dict[str, str]) -> SimpleProgramExecutionResult:
        try:
            process_output_data = subprocess.check_output(command, env=environment)
            exit_code = 0  # since no exception raised, exit code was zero
        except subprocess.CalledProcessError as exception:
            process_output_data = exception.output
            exit_code = exception.returncode
        return SimpleProgramExecutionResult(process_output_data, exit_code)
