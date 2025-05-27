import os
import sys


class StrictEnvironmentParser:
    """
    A simple parser of environment variables, where each one added is mandatory and treated as a string.
    The purpose of this class is to get similar behavior to argparse.ArgumentParser, where names of stuff
    to be read can be added and when they are missing the user will be told what they are missing.
    """
    def __init__(self):
        self._required_variable_names: set[str] = set()

    def add_argument(self, name: str) -> None:
        self._required_variable_names.add(name)

    def get_arguments(self) -> dict[str, str]:
        """
        Reads the names and values of the required argument
        variables into a dictionary aborts the program with a helpful message if any are missing.
        """
        read_environment_arguments: dict[str, str] = dict()
        missing_any_environment_variables = False
        for required_variable_name in self._required_variable_names:
            value = os.environ.get(required_variable_name)
            if value is None:
                print(f"[ENVPARSER] MISSING REQUIRED ENVIRONMENT VARIABLE: {required_variable_name}", file=sys.stderr)
                missing_any_environment_variables = True
            read_environment_arguments[required_variable_name] = value
        if missing_any_environment_variables:
            sys.exit(1)
        return read_environment_arguments
