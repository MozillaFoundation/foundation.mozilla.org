from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase
from unittest.mock import MagicMock

from delete_non_staff import delete_non_staff
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


class DeleteNonStaffTests(TestCase):

    def setUp(self):
        group = Group.objects.create(name='TestGroup')
        group.user_set.create(username='Sam')
        User.objects.bulk_create([
            User(username='Alex'),
            User(username='Bob', email='bob@mozillafoundation.org'),
            User(username='Alice', is_staff=True)
        ])

    def test_non_staff_is_deleted(self):
        """
        Test that only non_staff users are deleted
        """

        delete_non_staff()

        self.assertEqual(User.objects.count(), 3)
