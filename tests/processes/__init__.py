import os
import sys
import subprocess


def get_script_start_command(script_name: str, arguments: list[str] | None = None) -> list[str]:
    script_path = os.path.join(os.path.dirname(__file__), "scripts", script_name)
    assert os.path.exists(script_path), f"path doesn't exist {script_path}"
    start_command = [sys.executable, script_path] + (arguments or [])
    return start_command


def get_popen_for_script_with_pipes(script_name: str, arguments: list[str] | None = None) -> subprocess.Popen:
    """
    Opens a process for the script with the given name and arguments and does
    it with a pipe set for stdout and stdin so that both can be read.
    """
    start_command = get_script_start_command(script_name, arguments)
    process = subprocess.Popen(start_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process