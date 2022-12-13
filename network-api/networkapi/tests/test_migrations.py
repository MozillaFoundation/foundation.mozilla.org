from datetime import date, datetime, timezone
from io import StringIO
from unittest import skip

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import translation
from django.utils.translation.trans_real import (
    parse_accept_lang_header as django_parse_accept_lang_header,
)
from django.utils.translation.trans_real import to_language as django_to_language
from wagtail.core.models import Site
from wagtail_factories import SiteFactory

from networkapi.utility.redirects import redirect_to_default_cms_site
from networkapi.wagtailpages import (
    language_code_to_iso_3166,
    parse_accept_lang_header,
    to_language,
)

# from django.test.utils import override_settings


class MissingMigrationsTests(TestCase):
    def test_no_migrations_missing(self):
        """
        Ensure we didn't forget a migration
        """
        output = StringIO()
        call_command("makemigrations", interactive=False, dry_run=True, stdout=output)

        if output.getvalue() != "No changes detected\n":
            raise AssertionError("Missing migrations detected:\n" + output.getvalue())


class RedirectDefaultSiteDecoratorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Change the default site away from localhost
        self.original_default_site = Site.objects.get(is_default_site=True, hostname="localhost")
        self.original_default_site.is_default_site = False
        self.original_default_site.save()
        # Add a default site, and a secondary site.
        self.default_site = SiteFactory(hostname="default-site.com", is_default_site=True)
        self.secondary_site = SiteFactory(hostname="secondary-site.com")

    def test_redirect_decorator(self):
        """
        Test that the decorator redirects.
        """
        decorated_view = redirect_to_default_cms_site(lambda request: None)
        response = decorated_view(self.factory.get("/example/", HTTP_HOST="secondary-site.com"))
        self.assertEqual(response.status_code, 302)

    def test_redirect_decorator_doesnt_redirect(self):
        """
        Test that the redirect is triggered only when needed.
        """
        decorated_view = redirect_to_default_cms_site(lambda request: "untouched response")
        response = decorated_view(self.factory.get("/example/"))
        self.assertEqual(response, "untouched response")

    @skip("TODO: REENABLE: TEMPORARY SKIP TO MAKE PNI-AS-WAGTAIL LAUNCH POSSIBLE")
    # @override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_PNI_homepage_redirect_to_foundation_site(self):
        """
        Test that users gets redirected to PNI on the foundation site when they visit it from a non-default CMS site
        """
        response = self.client.get("/en/privacynotincluded/", HTTP_HOST="secondary-site.com")
        self.assertRedirects(
            response,
            "https://default-site.com/en/privacynotincluded/",
            fetch_redirect_response=False,
        )

    def tearDown(self):
        # Re-instante localhost as the default site
        self.original_default_site.is_default_site = True
        self.original_default_site.save()

        # Remove the Site Factories
        self.default_site.delete()
        self.secondary_site.delete()


class WagtailPagesTestCase(TestCase):
    def test_get_language_code_to_iso_3166(self):
        self.assertEqual(language_code_to_iso_3166("en-gb"), "en-GB")
        self.assertEqual(language_code_to_iso_3166("en-us"), "en-US")
        self.assertEqual(language_code_to_iso_3166("fr"), "fr")

    def test_to_language(self):
        self.assertEqual(to_language("en_US"), "en-US")

    def test_parse_accept_lang_header_returns_iso_3166_language(self):
        self.assertEqual(
            parse_accept_lang_header("en-GB,en;q=0.5"),
            (("en-GB", 1.0), ("en", 0.5)),
        )


class WagtailPagesIntegrationTestCase(TestCase):

    """
    Test that our overrides to Django translation functions work.
    """

    def test_to_language(self):
        self.assertEqual(django_to_language("fy_NL"), "fy-NL")

    def test_parse_accept_lang_header_returns_iso_3166_language(self):
        self.assertEqual(
            django_parse_accept_lang_header("fy-NL,fy;q=0.5"),
            (("fy-NL", 1.0), ("fy", 0.5)),
        )

    @skip("TODO: REMOVE: NOW DONE BY WAGTAIL")
    def test_reverse_produces_correct_url_prefix(self):
        translation.activate("fy-NL")
        url = reverse("buyersguide-home")
        self.assertTrue(url.startswith("/fy-NL/"))
        translation.deactivate()
