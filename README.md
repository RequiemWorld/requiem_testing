![Continuous Integration](https://github.com/RequiemWorld/requiem_testing/actions/workflows/continuous-integration.yml/badge.svg)
# Requiem Testing
A package to aid in automated end to end acceptance testing/release/distribution of software on the project. 
## Glossary
- **Networking**
  - **RelevantProcNetTCPEntry** -> A helper class for representing the values that we care about from entries in the /proc/net/tcp file in Linux. 
- **Peripherals** - Utilities for installing back-channels on the software that can be enabled during acceptance testing
  - **TimeForward** -> A representation of the amount of time to take time forward by.
  - **TimeForwardClock** -> A clock that can get the current time and add more time to it.
- **Processes** - Utilities to aid with process-related concerns.
    - **Process Existence Checking**
        - A function is provided for checking if a process exists which is distinct from a process being dead, and more relevant for what we want to check for on multiple platforms, because **1)** A zombie process is by definition dead but shows up as existing in /proc/{pid}. **2)** A zombie process is technically a thing on windows but a process will not show up as existing when it hasn't been reaped.
