import unittest
from datetime import timedelta
from requiem_testing.peripherals.time import TimeForward


class TestTimeForwardConstructionIntegrity(unittest.TestCase):

    def test_should_raise_value_error_when_time_delta_is_negative(self):
        with self.assertRaises(ValueError):
            TimeForward(timedelta(days=-1))

    def test_should_raise_value_error_when_time_delta_is_zero(self):
        with self.assertRaises(ValueError):
            TimeForward(timedelta(days=0))


class TestTimeForwardAddition(unittest.TestCase):

    def test_should_add_time_forwards_together_correctly(self):
        # 1 day + 1 day = 2 days
        added_together = TimeForward(timedelta(days=1)) + TimeForward(timedelta(days=1))
        self.assertEqual(timedelta(days=2), added_together.amount)
