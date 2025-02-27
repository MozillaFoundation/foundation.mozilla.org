from unittest.mock import MagicMock

from django.test import TestCase

from legacy_cms.utility.middleware import XRobotsTagMiddleware


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


class NormalizeLocaleMiddlewareTest(TestCase):
    def test_redirect_with_pt_br_language(self):
        # Simulate a request to a URL with 'pt-br' in the path
        response = self.client.get("/pt-br/?form=donate-header")

        # Assert that the middleware issues a redirect to the normalized URL
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/pt-BR/?form=donate-header")

    def test_redirect_with_fy_NL_language(self):
        # Simulate a request to a URL with 'fy-nl' in the path
        response = self.client.get("/fy-nl/?form=donate-header")

        # Assert that the middleware issues a redirect to the normalized URL
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/fy-NL/?form=donate-header")
