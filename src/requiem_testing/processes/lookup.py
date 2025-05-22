import os
import sys


def verify_process_exists(process_id: int) -> bool:
    """
    Verifies that a process exists based on if it can be looked up,
    which is a more forward way to look at what we want cross-platform.

    :raises NotImplementedError: If not compatible with the platform it has been called from (only Linux is supported right now).
    """
    if sys.platform != "linux":
        raise NotImplementedError(f"the only platform that is supported is Linux, not {sys.platform}")
    # A process can exist and be alive, a process can exist and be a zombie
    # A process that is a zombie is "dead" by definition, but that isn't what we care for.
    return os.path.exists(f"/proc/{process_id}")

