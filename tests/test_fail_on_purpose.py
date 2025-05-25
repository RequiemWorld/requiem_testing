import unittest


class TestIntentionallyFail(unittest.TestCase):
    def test_something(self):
        self.fail()