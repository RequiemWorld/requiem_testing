import unittest
import subprocess
from requiem_testing.processes.lookup import verify_process_exists
from . import get_script_start_command


class TestProcessExistenceVerificationFunction(unittest.TestCase):

    def test_should_return_true_when_there_is_a_process_started_matching_given_id(self):
        process = subprocess.Popen(get_script_start_command("sleep_forever.py"))
        self.assertTrue(verify_process_exists(process.pid))

    def test_should_return_false_after_process_has_died_naturally_and_exit_code_has_been_read(self):
        process = subprocess.Popen(get_script_start_command("empty_file.py"))
        process.wait()
        self.assertFalse(verify_process_exists(process.pid))
