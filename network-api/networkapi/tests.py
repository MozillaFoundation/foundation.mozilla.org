from io import StringIO

from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase, RequestFactory
from unittest.mock import MagicMock

from wagtail_factories import SiteFactory

from networkapi.utility.redirects import redirect_to_default_cms_site
from networkapi.utility.middleware import ReferrerMiddleware, XRobotsTagMiddleware


class ReferrerMiddlewareTests(TestCase):

    def setUp(self):
        referrer_middleware = ReferrerMiddleware('response')
        self.assertEqual(referrer_middleware.get_response, 'response')

    def test_requestProcessing(self):
        """
        Ensure that the middleware assigns a Referrer-Policy header to the response object
        """

        referrer_middleware = ReferrerMiddleware(MagicMock())
        response = referrer_middleware(MagicMock())
        response.__setitem__.assert_called_with('Referrer-Policy', 'same-origin')


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


class RedirectDefaultSiteDecoratorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.default_site = SiteFactory(hostname='default-site.com', is_default_site=True)
        self.secondary_site = SiteFactory(hostname="secondary-site.com")

    def test_redirect_decorator(self):
        """
        Test that the decorator redirects.
        """
        decorated_view = redirect_to_default_cms_site(lambda request: None)
        response = decorated_view(self.factory.get('/example/', HTTP_HOST='secondary-site.com'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_decorator_doesnt_redirect(self):
        """
        Test that the redirect is triggered only when needed.
        """
        decorated_view = redirect_to_default_cms_site(lambda request: "untouched response")
        response = decorated_view(self.factory.get('/example/'))
        self.assertEqual(response, "untouched response")

    def test_PNI_homepage_redirect_to_foundation_site(self):
        """
        Test that users gets redirected to PNI on the foundation site when they visit it from a non-default CMS site
        """
        response = self.client.get('/en/privacynotincluded/', HTTP_HOST='secondary-site.com')
        self.assertRedirects(
            response,
            "https://default-site.com/en/privacynotincluded/",
            fetch_redirect_response=False
        )

    class XRobotsTagMiddlewareTest(TestCase):
        def test_returns_response(self):
            xrobotstag_middleware = XRobotsTagMiddleware('response')
            self.assertEqual(xrobotstag_middleware.get_response, 'response')

        def test_sends_x_robots_tag(self):
            """
            Ensure that the middleware assigns an X-Robots-Tag to the response
            """

            xrobotstag_middleware = XRobotsTagMiddleware(MagicMock())
            response = xrobotstag_middleware(MagicMock())
            response.__setitem__.assert_called_with('X-Robots-Tag', 'noindex')
