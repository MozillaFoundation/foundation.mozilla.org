from django.test import TestCase, Client
from unittest.mock import MagicMock
from mezzanine.conf import settings

from networkapi.middleware import ReferrerMiddleware


class ReferrerMiddlewareTests(TestCase):

	def setUp(self):
		self.middleware = ReferrerMiddleware()
		self.request = MagicMock()
		self.response = MagicMock()

	def test_requestProcessing(self):
		"""
		Ensure that the middleware assigns a Referrer-Policy header to the response object
		"""

		response = self.middleware.process_response(self.request, self.response)
		response.__setitem__.assert_called_with('Referrer-Policy', 'same-origin')

