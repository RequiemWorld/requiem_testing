import unittest
from requiem_testing.peripherals.http import HTTPResponse


class TestHTTPResponseConstruction(unittest.TestCase):

    def test_should_construct_response_with_given_status_code(self):
        response_one = HTTPResponse(200, "", {}, b"")
        response_two = HTTPResponse(201, "", {}, b"")

        self.assertEqual(200, response_one.status_code)
        self.assertEqual(201, response_two.status_code)

    def test_should_construct_response_with_given_reason_phrase(self):
        response_one = HTTPResponse(200, "SOME TEXT 1", {}, b"")
        response_two = HTTPResponse(200, "SOME TEXT 2", {}, b"")
        self.assertEqual("SOME TEXT 1", response_one.reason_phrase)
        self.assertEqual("SOME TEXT 2", response_two.reason_phrase)

    def test_should_construct_response_with_given_headers(self):
        response = HTTPResponse(502, "BAD GATEWAY", {"a": "b"}, b"")
        self.assertEqual({"a": "b"}, response.headers)


class TestHTTPResponseCopyingMethod(unittest.TestCase):

    def test_should_return_different_instance_of_http_response_object_and_not_same_one(self):
        response = HTTPResponse(200, "OK", {}, b"")
        self.assertIsNot(response, response.copy())

    def test_should_return_copy_of_headers_dictionary_and_not_exact_same_one(self):
        response = HTTPResponse(200, "OK", {}, b"")
        response_copy = response.copy()
        response.headers["Header"] = "Value"
        self.assertIn("Header", response.headers)
        self.assertNotIn("Header", response_copy.headers)


class TestHTTPResponseContentLengthFillingMethod(unittest.TestCase):

    @staticmethod
    def _make_response(content: bytes, headers: dict[str, str] | None = None) -> HTTPResponse:
        if headers is None:
            headers = {}
        return HTTPResponse(200, "OK", headers, content)

    def test_should_update_content_length_header_when_already_present_and_length_has_changed(self):
        response = self._make_response(b"123", {"Content-Length": "3"})
        self.assertEqual(response.headers["Content-Length"], "3")
        response.content += b"456"
        response.fill_content_length()
        self.assertEqual(response.headers["Content-Length"], "6")

    def test_should_add_content_length_header_with_length_of_content_when_does_not_already_exist(self):
        response = self._make_response(b"abc",)
        self.assertNotIn("Content-Length", response.headers)
        response.fill_content_length()
        self.assertEqual("3", response.headers["Content-Length"])

    def test_should_raise_value_error_when_there_is_no_actual_content_to_write_length_of(self):
        response = self._make_response(b"")
        with self.assertRaises(ValueError):
            response.fill_content_length()
