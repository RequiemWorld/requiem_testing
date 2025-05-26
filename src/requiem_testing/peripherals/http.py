import enum
import json
from json import JSONDecodeError
from typing import Awaitable, Callable


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
        header_name, header_value = header_line_data.decode().split(":", 1)
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


# [DESIGN WORK IN PROGRESS]
class HTTPMethod(enum.Enum):
    ANY = "ANY"  # this is trashy, however, this enum is also used for the router for now, and this is simple
    GET = "GET"
    POST = "POST"


# [DESIGN WORK IN PROGRESS]
class HTTPRequest:
    def __init__(self, method: HTTPMethod, path: str, headers: dict[str, str], content: bytes):
        self.path = path
        self.headers = headers
        self.method = method
        self.content = content

    def copy(self) -> "HTTPRequest":
        return HTTPRequest(self.method, self.path, self.headers.copy(), self.content)

    def json(self) -> list | dict:
        """
        Assumes the request body has no encoding and is serialized JSON, then deserializes it.
        :raises ValueError: when the content in the body is not json or deserialization has failed.
        """
        try:
            return json.loads(self.content.decode())
        except JSONDecodeError as e:
            raise ValueError from e


# [DESIGN WORK IN PROGRESS]
class HTTPResponse:
    def __init__(self, status_code: int, reason_phrase: str, headers: dict[str, str], content: bytes):
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.headers = headers
        self.content = content

    def copy(self) -> "HTTPResponse":
        return HTTPResponse(self.status_code, self.reason_phrase, self.headers.copy(), self.content)

    def fill_content_length(self) -> None:
        """
        Measures the length of the content data and changes the Content-Length header value to match.

        :raises ValueError: When there is no content present to write the length of.
        """
        if self.content == b"":
            raise ValueError("content is empty and no length content length should be written")

        self.headers["Content-Length"] = str(len(self.content))


# [DESIGN WORK IN PROGRESS]
RequestHandler = Callable[[HTTPRequest], Awaitable[HTTPResponse]]
class AsyncHTTPRouter:
    """
    A simple facility for mapping methods and paths to request handlers.
    """
    def __init__(self):
        self._paths_to_handlers_map: dict[tuple[str, HTTPMethod], RequestHandler] = dict()

    def _add_handler(self, path: str, method: HTTPMethod, handler: RequestHandler) -> None:

        """
        :raises ValueError: When a handler has already been added for the path matching any method.
        """
        if (path, HTTPMethod.ANY) in self._paths_to_handlers_map:
            raise ValueError("this path already has a handled added that matches ANY path and method")
        self._paths_to_handlers_map[path, method] = handler

    def add_handler_for_any(self, path: str, handler: RequestHandler):
        """
        Given a path and request handler, will map it so that any request for
        that path under any method will get handled by it.
        """
        self._add_handler(path, HTTPMethod.ANY, handler)

    def add_handler_for_get(self, path: str, handler: RequestHandler) -> None:
        """
        Add a request handler for the given path, for get requests specifically.

        :raises ValueError: When a handler has already been added for the path matching any method.
        """
        self._add_handler(path, HTTPMethod.GET, handler)

    def add_handler_for_post(self, path: str, handler: RequestHandler) -> None:
        self._add_handler(path, HTTPMethod.POST, handler)

    def get_handler_for_path(self, path: str, method: HTTPMethod) -> RequestHandler | None:
        handler_for_any_method = self._paths_to_handlers_map.get((path, HTTPMethod.ANY))
        if handler_for_any_method is not None:
            return handler_for_any_method
        return self._paths_to_handlers_map.get((path, method))

