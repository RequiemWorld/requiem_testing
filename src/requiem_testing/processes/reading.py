import abc

class ProcessLineOutputReader(abc.ABC):

    @abc.abstractmethod
    def read_stdout_line(self, timeout: int | float) -> str:
        """
        Reads data from the stdout of the process until a line is found, aborting
        and raising a TimeOut exception if a line is not found in the given timeout period.

        - If there is an empty line, then an empty string is returned instead of returning the line separator.
        - If there is no more data to be read, then stderr EOFError will be raised instead of returning an empty string.

        :raises EOFError: If there are no lines in the internal buffer, and there is no more data to be read from stdout.
        :raises TimeoutError: If there is no data to be read from stdout, or the data read doesn't form a line in the given time.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def read_stderr_line(self, timeout: int | float) -> str:
        """
        Reads data from the stderr of the process until a line is found, aborting
        and raising a TimeOut exception if a line is not found in the given timeout period.

        - If there is an empty line, then an empty string is returned instead of returning the line separator.
        - If there is no more data to be read, then stderr EOFError will be raised instead of returning an empty string.

        :raises EOFError: If there are no lines in the internal buffer, and there is no more data to be read from stderr.
        :raises TimeoutError: If there is no data to be read from stderr, or the data read doesn't form a line in the given time.
        """
        raise NotImplementedError