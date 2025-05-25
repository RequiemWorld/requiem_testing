import unittest
from requiem_testing.peripherals.http import write_status_line
from requiem_testing.peripherals.http import write_header_lines


class TestStatusLineWritingFunction(unittest.TestCase):

    def test_should_write_out_status_code_number_as_expected(self):
        self.assertEqual(b"http/1.1 301 redirect?\r\n", write_status_line(301, "redirect?", "http/1.1"))

    def test_should_write_out_status_reason_string_in_same_casing_as_given(self):
        # not sure what the capitalization is considered best practice to be, so designing it to write it out as given.
        self.assertEqual(b"HTTP/1.1 404 NoT FoUnD\r\n", write_status_line(404, "NoT FoUnD", "HTTP/1.1"))

    def test_should_write_out_http_version_string_in_same_casing_as_given(self):
        self.assertEqual(b"HttP/1.1 200 OK\r\n", write_status_line(200, "OK", "HttP/1.1"))

    def test_should_write_everything_out_ending_in_crlf(self):
        self.assertTrue(write_status_line(200, "OK", "HTTP/1.1").endswith(b"\r\n"))


class TestHeaderLinesWritingFunction(unittest.TestCase):

    def test_should_write_single_header_out_and_have_it_end_with_crlf_crlf(self):
        self.assertEqual(b"Name: value\r\n\r\n", write_header_lines([("Name", "value")]))

    def test_should_write_single_header_out_with_single_space_after_colon(self):
        self.assertEqual(b"Name: value\r\n\r\n", write_header_lines([("Name", "value")]))

    def test_should_write_multiple_headers_out_with_crlf_between_them(self):
        headers = [("one", "1"), ("two", "2")]
        self.assertEqual(b"one: 1\r\ntwo: 2\r\n\r\n", write_header_lines(headers))

    def test_should_write_multiple_headers_out_ending_with_crlf_crlf(self):
        headers = [("Name-1", "value1"), ("Name-2", "value2")]
        self.assertEqual(b"Name-1: value1\r\nName-2: value2\r\n\r\n", write_header_lines(headers))

    def test_should_write_header_names_out_with_same_casing_as_passed_in(self):
        headers = [("AbC", "def"), ("EfG", "hij")]
        self.assertEqual(b"AbC: def\r\nEfG: hij\r\n\r\n", write_header_lines(headers))

    def test_should_write_header_values_out_with_same_casing_as_passed_in(self):
        headers = [("jkl", "MnO"), ("pqr", "StU")]
        self.assertEqual(b"jkl: MnO\r\npqr: StU\r\n\r\n", write_header_lines(headers))
