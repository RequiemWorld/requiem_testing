![Continuous Integration](https://github.com/RequiemWorld/requiem_testing/actions/workflows/continuous-integration.yml/badge.svg?no-cache)
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
- **Experimental** - Utilities that are being designed/tested out and may or may not be here to stay. These utilities may not be adequately tested but the idea is to get the base idea figured out before going further.
  - **SimpleProgramExecutor** - A utility to execute programs with a given command/arguments and environment variables
  - **SimpleProgramExecutionResult** - A utility for taking process output and asserting that lines are in it regardless of platform.
  - **CommandLineAcceptanceTestCase** - A base class for making base classes for the acceptance testing of command line applications
    - Not every application on the project is going to be fit for having the four-layer architecture of test case/dsl/driver/sut and command line applications are one of these. The simplest place to work out writing any acceptance tests is with command line applications.
    - **Note 1**: This style of acceptance test is meant to test something that is very explicitly a command line application that does not require any user input past given arguments. 
    - **Note 2**: This should be able to start and run the application without having to know exactly where it is and how to execute it e.g. it should be able to run a hello_world.py or a hello_world.exe.
    - **Note 3**: The current idea is to have the subclass that will form the base class to inherit for testing the specific application to setup an argument parser, and to setup information about the program to execute such as the base part of the start command. For example: Regardless of print_text.py or print_text.exe, the test should be able to run something like self.execute("--text-to-print value")
    - **Note 4**: In different styles of acceptance tests, it will be desirable to have the test case start the application at least once from somewhere, and this may pave the way for a similar approach.

## Versioning Notice

The versioning of this is not going to be consistent while this is in development and on 0.x.x versions, anything in this repository that doesn't have tests should be expected to break. Various stuff in here is actively being designed and developed, and being driven by the development of stuff external to this repository, additions to anything that might be temporary will result in a version increase, even if the stuff added isn't tested.
