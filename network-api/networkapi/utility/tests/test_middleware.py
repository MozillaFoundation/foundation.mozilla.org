from unittest.mock import MagicMock

from django.test import TestCase

from networkapi.utility.middleware import ReferrerMiddleware, XRobotsTagMiddleware


class ReferrerMiddlewareTests(TestCase):
    def setUp(self):
        referrer_middleware = ReferrerMiddleware("response")
        self.assertEqual(referrer_middleware.get_response, "response")

    def test_requestProcessing(self):
        """
        Ensure that the middleware assigns a Referrer-Policy header to the response object
        """

        referrer_middleware = ReferrerMiddleware(MagicMock())
        response = referrer_middleware(MagicMock())
        response.__setitem__.assert_called_with("Referrer-Policy", "strict-origin-when-cross-origin")


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
