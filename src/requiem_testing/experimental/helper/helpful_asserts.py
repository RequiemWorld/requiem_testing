

def assert_string_ends_with(string: str, ending: str, msg: str | None = None) -> None:
    """
    Asserts that a string ends with another string, raising
    an assertion error that says what the actual string is that doesn't end with it.

    :raises AssertionError: if the given string doesn't end with the given ending.
    """
    if msg is None:
        assertion_message = f"ending {ending} not found in {string}"
    else:
        assertion_message = msg

    assert string.endswith(ending), assertion_message
