from time import sleep
from django.test import TestCase

from networkapi.utility.decorators import debounce_and_throttle


@debounce_and_throttle(1, 3)
def test_fn(context):
    context.times_called += 1


class DebounceThrottleTestCase(TestCase):
    def tearDown(self):
        # cool down so the timeout doesn't affect other tests
        sleep(3)

    def test_called(self):
        self.times_called = 0

        test_fn(self)

        # Not called yet
        self.assertEqual(self.times_called, 0)

        sleep(2)

        # Was called after debounce timeout
        self.assertEqual(self.times_called, 1)

        # Cooldown for

    def test_called_once(self):
        self.times_called = 0

        # Call the function multiple times
        test_fn(self)
        test_fn(self)
        test_fn(self)

        sleep(2)

        # After debounce timeout, it should have only been called once
        self.assertEqual(self.times_called, 1)

    def test_timeout(self):
        self.times_called = 0

        # Call the function and wait for it to execute once
        test_fn(self)
        sleep(2)
        self.assertEqual(self.times_called, 1)

        # call the function again, but the timeout should prevent execution
        test_fn(self)
        sleep(2)
        self.assertEqual(self.times_called, 1)
