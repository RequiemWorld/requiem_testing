import unittest
from datetime import datetime, timedelta
from requiem_testing.peripherals.time import TimeForward
from requiem_testing.peripherals.time import TimeForwardClock


class TestTimeForwardClockTimeAddingAndGettingMethods(unittest.TestCase):
    def setUp(self):
        self._default_time = datetime(year=2000, month=1, day=1)
        self._time_provider = lambda: self._default_time
        self._default_clock = TimeForwardClock(self._time_provider)

    def test_should_return_actual_current_time_by_default(self):
        self.assertEqual(self._default_time, self._default_clock.get_time())

    def test_should_return_current_time_plus_only_time_forward_added(self):
        self._default_clock.add_time(TimeForward(timedelta(days=1)))
        self.assertEqual(self._default_time + timedelta(days=1), self._default_clock.get_time())

    def test_should_return_current_time_plus_sum_of_multiple_time_forwards_added(self):
        self._default_clock.add_time(TimeForward(timedelta(days=2)))
        self._default_clock.add_time(TimeForward(timedelta(days=4)))
        self._default_clock.add_time(TimeForward(timedelta(days=8)))
        self.assertEqual(self._default_time + timedelta(days=14), self._default_clock.get_time())