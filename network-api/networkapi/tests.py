from django.core.management import call_command
from django.test import TestCase
from unittest.mock import MagicMock

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


class MissingMigrationsTests(TestCase):

    def test_no_migrations_missing(self):
        """
        Ensure we didn't forget a migration
        """
        call_command('makemigrations', interactive=False, dry_run=True, check_changes=True)
