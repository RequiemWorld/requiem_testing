import abc
import shlex
import pytest
import unittest
import argparse
from dataclasses import dataclass
from requiem_testing.experimental.envparse import StrictEnvironmentParser
from requiem_testing.experimental.execution import SimpleProgramExecutor, SimpleProgramExecutionResult


def parse_command_from_normal_command_string(normal_command: str) -> list[str]:
    return shlex.split(normal_command)


@dataclass
class CommandLineConfiguration:
    base_start_command: list[str]


class CommandLineAcceptanceTestCase(unittest.TestCase, abc.ABC):
    configuration: CommandLineConfiguration
    environment_parser: StrictEnvironmentParser

    @pytest.fixture(autouse=True, scope="function")
    def _before_each_test(self):
        self.environment_parser = StrictEnvironmentParser()
        self.configure_envparse(self.environment_parser)
        self.configuration = self.configure_test_case()

    def configure_envparse(self, parser: StrictEnvironmentParser) -> None:
        """
        Configures an environment parser used to parse arguments required
        for knowing how to start and test the application.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def configure_test_case(self) -> CommandLineConfiguration:
        raise NotImplementedError

    def execute(self, arguments: list[str], environment: dict[str, str] | None = None) -> SimpleProgramExecutionResult:
        executor = SimpleProgramExecutor()
        return executor.execute_program(self.configuration.base_start_command + arguments, environment or {})
