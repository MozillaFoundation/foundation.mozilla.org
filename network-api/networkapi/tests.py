from django.contrib.auth.models import User, Group
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


class DeleteNonStaffTest(TestCase):

    def setUp(self):
        User.objects.create(username='Alex'),

    def test_non_staff_is_deleted(self):
        """
        Simple users are deleted
        """

        call_command('delete_non_staff')

        self.assertEqual(User.objects.count(), 0)


class IsStaffNotDeletedTest(TestCase):

    def setUp(self):
        User.objects.create(username='Alex', is_staff=True)

    def test_is_staff_not_deleted(self):
        """
        Users with 'is_staff' flag at True are not deleted
        """

        call_command('delete_non_staff')

        self.assertEqual(User.objects.count(), 1)


class InGroupNotDeletedTest(TestCase):

    def setUp(self):
        group = Group.objects.create(name='TestGroup')
        group.user_set.create(username='Alex')

    def test_in_group_not_deleted(self):
        """
        Users in a group are not deleted
        """

        call_command('delete_non_staff')

        self.assertEqual(User.objects.count(), 1)


class MozillaFoundationUsersNotDeletedTest(TestCase):

    def setUp(self):
        User.objects.create(username='Alex', email='alex@mozillafoundation.org')

    def test_mozilla_foundation_users_not_deleted(self):
        """
        Mozilla Foundation Users are not deleted
        """

        call_command('delete_non_staff')

        self.assertEqual(User.objects.count(), 1)
