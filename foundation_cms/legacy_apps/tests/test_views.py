from django.test import TestCase, override_settings
from wagtail.models import Site

from foundation_cms.legacy_apps.mozfest.factory import MozfestHomepageFactory
from foundation_cms.legacy_apps.wagtailpages.factory.blog import BlogPageFactory
from foundation_cms.legacy_apps.wagtailpages.factory.homepage import (
    WagtailHomepageFactory,
)


class TestApplePayDomainAssociationView(TestCase):
    """
    Keys are set with override_settings rather than by assigning to
    django.conf.settings directly.

    Direct assignment is never undone, so it leaked into every later test in
    the same process. These tests then only passed in one particular order --
    and under `pytest --splits ... -n ...` the suite is distributed across
    shards and xdist workers, so that order is not guaranteed. Adding tests
    anywhere in the repo could reshuffle it and break them.
    """

    def setUp(self):
        self.site = Site.objects.first()
        self.foundation_homepage = WagtailHomepageFactory()
        self.mozfest_homepage = MozfestHomepageFactory()
        self.blog_page = BlogPageFactory()
        self.view_url = "/.well-known/apple-developer-merchantid-domain-association"

    def _serve_from(self, root_page):
        self.site.root_page = root_page
        self.site.save()
        return self.client.get(self.view_url)

    @override_settings(APPLE_PAY_DOMAIN_ASSOCIATION_KEY_FOUNDATION="test_foundation_key")
    def test_foundation_site_request(self):
        """
        Make sure the view returns the foundation specific key,
        when a request is made from the foundation site.
        """
        response = self._serve_from(self.foundation_homepage)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "test_foundation_key")

    @override_settings(APPLE_PAY_DOMAIN_ASSOCIATION_KEY_FOUNDATION="")
    def test_foundation_site_request_with_no_key_set(self):
        """
        If no foundation site key is set, the view should return a
        'key not found' error message.
        """
        response = self._serve_from(self.foundation_homepage)

        self.assertEqual(response.status_code, 501)
        self.assertEqual(response.content.decode(), "Key not found. Please check environment variables.")

    @override_settings(APPLE_PAY_DOMAIN_ASSOCIATION_KEY_MOZFEST="test_mozfest_key")
    def test_mozfest_site_request(self):
        """
        Make sure the view returns the mozfest specific key,
        when a request is made from the mozfest site.
        """
        response = self._serve_from(self.mozfest_homepage)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "test_mozfest_key")

    @override_settings(APPLE_PAY_DOMAIN_ASSOCIATION_KEY_MOZFEST="")
    def test_mozfest_site_request_with_no_key_set(self):
        """
        If no mozfest site key is set, the view should return a
        'key not found' error message.

        This previously served from self.foundation_homepage, so it exercised
        the foundation branch of the view and never tested the mozfest one.
        """
        response = self._serve_from(self.mozfest_homepage)

        self.assertEqual(response.status_code, 501)
        self.assertEqual(response.content.decode(), "Key not found. Please check environment variables.")

    def test_request_from_other_site(self):
        """
        Making sure that any request from a site that has neither a
        'WagtailHomePage' or a 'MozfestHomePage' set as the root,
        returns a 400 error.
        """
        response = self._serve_from(self.blog_page)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Request site not recognized.")
