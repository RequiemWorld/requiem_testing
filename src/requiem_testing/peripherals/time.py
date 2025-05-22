from typing import Callable
from datetime import datetime
from datetime import timedelta


class TimeForward:
    """
    A value object to wrap around TimeDelta and assure that time can only go forward.
    """
    def __init__(self, amount: timedelta):
        if amount <= timedelta(0):
            raise ValueError("the amount for a time forward must be greater than zero")
        self._amount = amount

    def __add__(self, other: "TimeForward"):
        return TimeForward(self._amount + other.amount)

    @property
    def amount(self) -> timedelta:
        return self._amount


# Inspired by:
# (Acceptance Testing for Continuous Delivery by Dave Farley #AgileIndia2019)
# https://youtu.be/Rmz3xobXyV4?si=FEJAWS757Ql__Lvq&t=4597
# https://technology.lmax.com/posts/testing-at-lmax-time-travel-and-the-tardis/
class TimeForwardClock:
    """
    A clock meant to be used for time travel testing. Time travel testing is meant to
    test real world conditions where time can only travel forward.
    """

    def __init__(self, time_provider: Callable[[], datetime]):
        """
        :param time_provider: Something that can be called that will return the current time.
        """
        self._time_provider = time_provider
        self._time_forward_amount: TimeForward | None = None

    def add_time(self, forward: TimeForward):
        """
        Add a time forward to combine with the time when gotten from the system.
        """
        if self._time_forward_amount is None:
            self._time_forward_amount = forward
            return
        self._time_forward_amount += forward

    def get_time(self) -> datetime:
        """
        Get the current time plus the time added to forward it by.
        """
        current_time = self._time_provider()
        if self._time_forward_amount is not None:
            current_time += self._time_forward_amount.amount
        return current_time