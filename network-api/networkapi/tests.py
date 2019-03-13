from io import StringIO

from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase
from unittest.mock import MagicMock, patch

from networkapi.utility.middleware import ReferrerMiddleware


class ReferrerMiddlewareTests(TestCase):

    @patch('networkapi.utility.middleware.ReferrerMiddleware')
    def setUp(self):
        referrer_middleware = ReferrerMiddleware('response')
        self.assertEqual(referrer_middleware.get_response, 'response')

    def test_requestProcessing(self):
        """
        Ensure that the middleware assigns a Referrer-Policy header to the response object
        """

        request = MagicMock()
        referrer_middleware = ReferrerMiddleware(MagicMock())
        response = referrer_middleware(request)
        self.assertEqual(response['Referrer-Policy'], 'same-origin')


class MissingMigrationsTests(TestCase):

    def test_no_migrations_missing(self):
        """
        Ensure we didn't forget a migration
        """
        output = StringIO()
        call_command('makemigrations', interactive=False, dry_run=True, stdout=output)

        if output.getvalue() != "No changes detected\n":
            raise AssertionError("Missing migrations detected:\n" + output.getvalue())


class DeleteNonStaffTest(TestCase):

    def setUp(self):
        User.objects.create(username='Alex'),

    def test_non_staff_is_deleted(self):
        """
        Simple users are deleted
        """

        call_command('delete_non_staff', '--now')

        self.assertEqual(User.objects.count(), 0)


class IsStaffNotDeletedTest(TestCase):

    def setUp(self):
        User.objects.create(username='Alex', is_staff=True)

    def test_is_staff_not_deleted(self):
        """
        Users with 'is_staff' flag at True are not deleted
        """

        call_command('delete_non_staff', '--now')

        self.assertEqual(User.objects.count(), 1)


class InGroupNotDeletedTest(TestCase):

    def setUp(self):
        group = Group.objects.create(name='TestGroup')
        group.user_set.create(username='Alex')

    def test_in_group_not_deleted(self):
        """
        Users in a group are not deleted
        """

        call_command('delete_non_staff', '--now')

        self.assertEqual(User.objects.count(), 1)


class MozillaFoundationUsersNotDeletedTest(TestCase):

    def setUp(self):
        User.objects.create(username='Alex', email='alex@mozillafoundation.org')

    def test_mozilla_foundation_users_not_deleted(self):
        """
        Mozilla Foundation Users are not deleted
        """

        call_command('delete_non_staff', '--now')

        self.assertEqual(User.objects.count(), 1)
