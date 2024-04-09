from unittest.mock import MagicMock

from django.test import TestCase

from networkapi.utility.middleware import XRobotsTagMiddleware

class XRobotsTagMiddlewareTest(TestCase):
    def test_returns_response(self):
        xrobotstag_middleware = XRobotsTagMiddleware("response")
        self.assertEqual(xrobotstag_middleware.get_response, "response")

    def test_sends_x_robots_tag(self):
        """
        Ensure that the middleware assigns an X-Robots-Tag to the response
        """

        xrobotstag_middleware = XRobotsTagMiddleware(MagicMock())
        response = xrobotstag_middleware(MagicMock())
        response.__setitem__.assert_called_with("X-Robots-Tag", "noindex")
