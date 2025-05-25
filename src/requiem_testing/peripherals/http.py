

def parse_start_line(line_data: bytes) -> tuple[str, str, str]:
    """
    Takes the data for the first line of a request and parses out the strings for
    the method, path, and version, regardless of if it ends in CRLF or not.

    :param line_data: The value of the first line in the request, with, or without \r\n on the end.
    :raises ValueError: When the line_data contains more than three spaces.
    """
    if line_data.count(b" ") > 3:
        raise ValueError("the first line should not have more than three spaces!")
    method, path, version = line_data.decode().lower().rstrip("\r\n").split(" ")
    return method, path, version


def parse_header_lines(header_lines_data: bytes) -> dict[str, str]:
    """
    Takes the data for the lines of headers and parses the names and
    values and normalizes the header names to Title-Case.

    :param header_lines_data: The data for the header names and values separated by CRLF (\r\n). The data may end in \\r\\n\\r\\n.
    :raises ValueError: When the header line data doesn't have a colon in it for separating the name and value.
    """
    headers = {}
    header_lines = [line_data for line_data in header_lines_data.split(b"\r\n") if line_data != b""]
    for header_line_data in header_lines:
        header_name, header_value = header_line_data.decode().split(":")
        headers[header_name.title()] = header_value.lstrip(" ")
    return headers


def write_status_line(status_code: int, status_reason: str, http_version: str) -> bytes:
    """
    Writes out the http version, status code, and status reason ending with CRLF. All text inputs
    will be written out as is in the same casing.

    :param status_code: The number for the status (for example, 404)
    :param status_reason: The reason for the status (for example, NOT FOUND)
    :param http_version: The http version (for example, http/1.1)
    """
    return f"{http_version} {status_code} {status_reason}\r\n".encode()


def write_header_lines(headers: list[tuple[str, str]]) -> bytes:
    """
    Writes out the header lines, separated by CRLF, ending with a final CRLF to denote the end of the header lines.

    :param headers: A list tuples of header names and header values to be written out as is.
    """
    header_lines_data = b""
    for header_name, header_value in headers:
        header_lines_data += header_name.encode() + b": " + header_value.encode() + b"\r\n"
    header_lines_data += b"\r\n"
    return header_lines_data
