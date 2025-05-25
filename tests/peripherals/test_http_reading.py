import unittest
from requiem_testing.peripherals.http import parse_start_line
from requiem_testing.peripherals.http import parse_header_lines


class TestHTTPHeaderLinesParsingFunction(unittest.TestCase):

    def test_should_be_able_to_read_multiple_headers_that_have_no_spaces_at_start_of_field_value(self):
        self.assertEqual({"Name1": "abc" ,"Name2": "efg"}, parse_header_lines(b"Name1:abc\r\nName2:efg"))

    def test_should_be_able_to_read_multiple_headers_that_have_multiple_spaces_at_start_of_field_value(self):
        self.assertEqual({"Name1": "abc" ,"Name2": "efg"}, parse_header_lines(b"Name1:  abc\r\nName2:  efg"))

    def test_should_read_header_names_in_any_casing_and_normalize_them_to_title_case_in_returned_dictionary(self):
        self.assertEqual({"Name": "hij"}, parse_header_lines(b"NaMe: hij"))
        self.assertEqual({"Content-Type": "hij"}, parse_header_lines(b"content-type: hij"))

    def test_should_be_able_to_read_headers_when_last_header_in_data_ends_with_a_carriage_return_and_line_feed(self):
        self.assertEqual({"Header": "Value"}, parse_header_lines(b"Header: Value\r\n"))


class TestHTTPRequestStartLineParsingFunction(unittest.TestCase):

    def test_should_read_method_and_read_it_into_lowercase_regardless_of_casing(self):
        self.assertEqual("get", parse_start_line(b"get / HTTP/1.1")[0])
        self.assertEqual("get", parse_start_line(b"gEt / HTTP/1.1")[0])

    def test_should_read_path_and_read_it_into_lowercase_regardless_of_casing(self):
        self.assertEqual("/path1", parse_start_line(b"get /path1 HTTP/1.1")[1])
        self.assertEqual("/path1", parse_start_line(b"gEt /paTh1 HTTP/1.1")[1])

    def test_should_read_version_and_read_it_into_lowercase_regardless_of_casing(self):
        self.assertEqual("http/1.1", parse_start_line(b"gEt /paTh1 HTTP/1.1")[2])
        self.assertEqual("http/1.1", parse_start_line(b"gEt /paTh1 http/1.1")[2])

    def test_should_raise_value_error_when_line_data_has_more_than_three_spaces(self):
        with self.assertRaises(ValueError):
            parse_start_line(b"get /path1  HTTP/1.1")
        with self.assertRaises(ValueError):
            parse_start_line(b"get  /path1 HTTP/1.1")
        with self.assertRaises(ValueError):
            parse_start_line(b"get /path1 HTTP/1.1 ")

    def test_should_be_able_to_parse_start_line_even_when_it_ends_with_carriage_return_and_line_feed(self):
        self.assertEqual("get", parse_start_line(b"gEt /paTh1 http/1.1\r\n")[0])
        self.assertEqual("/path1", parse_start_line(b"gEt /paTh1 http/1.1\r\n")[1])
        self.assertEqual("http/1.1", parse_start_line(b"gEt /paTh1 http/1.1\r\n")[2])
