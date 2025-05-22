import unittest
import subprocess
from requiem_testing.processes.lookup import verify_process_exists
from . import get_script_start_command


class TestProcessExistenceVerificationFunctionLinux(unittest.TestCase):

    # should fail fast if the process somehow doesn't exist
    @staticmethod
    def _check_if_process_is_zombie(process_id: int):
        # Example: 4047148 (firefox) S 2798704 ...
        with open(f"/proc/{process_id}/stat") as f:
            relevant_column = f.read().split(" ")[2]
            return relevant_column == "Z"

    def _wait_for_process_to_become_zombie(self, process_id: int) -> None:
        while True:
            if self._check_if_process_is_zombie(process_id):
                return

    def test_should_return_true_for_process_that_is_a_zombie_ie_has_not_been_reaped_on_linux(self):
        # resources which were owned by a zombie process should be freed, but the process will
        # still exist in the kernel and more notably can be found in /proc/{pid}, just with a Z in a column in the stat file.
        process = subprocess.Popen(get_script_start_command("empty_file.py"))
        # if we wait for it to die with wait, then we'll reap it, and it won't be a zombie, so we have to check on it separately
        self._wait_for_process_to_become_zombie(process.pid)
        self.assertTrue(verify_process_exists(process.pid))