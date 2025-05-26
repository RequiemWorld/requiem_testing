import unittest
from requiem_testing.peripherals.http import HTTPMethod
from requiem_testing.peripherals.http import HTTPRequest

class TestHTTPRequestConstruction(unittest.TestCase):
    def test_should_construct_request_with_given_method(self):
        request_get = HTTPRequest(HTTPMethod.GET, "/", {}, b"")
        request_post = HTTPRequest(HTTPMethod.POST, "/", {}, b"")
        self.assertIs(request_get.method, HTTPMethod.GET)
        self.assertIs(request_post.method, HTTPMethod.POST)

    def test_should_construct_request_with_given_path(self):
        request = HTTPRequest(HTTPMethod.GET, "/my/path/123", {}, b"")
        self.assertEqual("/my/path/123", request.path)

    def test_should_construct_request_with_given_headers(self):
        request = HTTPRequest(HTTPMethod.GET, "/", {"header": "value"}, b"")
        self.assertEqual({"header": "value"}, request.headers)

    def test_should_construct_request_with_given_content(self):
        request = HTTPRequest(HTTPMethod.GET, "/", {"header": "value"}, b"123content")
        self.assertEqual(b"123content", request.content)


class TestHTTPRequestCopyMethod(unittest.TestCase):
    def setUp(self):
        self._http_request = HTTPRequest(HTTPMethod.GET, "/my/path", {"a": "b"}, b"c")
        self._copied_http_request = self._http_request.copy()

    def test_should_return_copy_of_headers_dictionary_and_not_exact_same_one(self):
        self.assertIsNot(self._http_request.headers, self._copied_http_request.headers)

    def test_should_return_different_instance_of_http_request_object_and_not_same_one(self):
        self.assertIsNot(self._http_request, self._copied_http_request)

    def test_should_return_http_request_object_with_equal_method_path_headers_and_content(self):
        self.assertEqual(HTTPMethod.GET, self._copied_http_request.method)
        self.assertEqual("/my/path", self._copied_http_request.path)
        self.assertEqual({"a": "b"}, self._copied_http_request.headers)
        self.assertEqual(b"c", self._copied_http_request.content)


class TestHTTPRequestJsonReadingMethod(unittest.TestCase):
    def test_should_deserialize_and_return_dictionary_contained_in_request_body(self):
        request = HTTPRequest(HTTPMethod.GET, "/some/path", {}, b'{"a": "b"}')
        self.assertEqual(request.json(), {"a": "b"})

    def test_should_deserialize_and_return_list_contained_in_request_body(self):
        request = HTTPRequest(HTTPMethod.GET, "/some/path", {}, b'["a", "b"]')
        self.assertEqual(["a", "b"], request.json())

    def test_should_raise_value_error_when_data_in_request_content_is_not_json(self):
        request = HTTPRequest(HTTPMethod.GET, "/some/path", {}, b'some content')
        with self.assertRaises(ValueError):
            request.json()
