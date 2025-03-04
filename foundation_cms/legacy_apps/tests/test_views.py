from django.conf import settings
from django.test import TestCase
from wagtail.models import Site

from foundation_cms.legacy_apps.mozfest.factory import MozfestHomepageFactory
from foundation_cms.legacy_apps.wagtailpages.factory.blog import BlogPageFactory
from foundation_cms.legacy_apps.wagtailpages.factory.homepage import (
    WagtailHomepageFactory,
)


class TestApplePayDomainAssociationView(TestCase):
    def setUp(self):
        self.site = Site.objects.first()
        self.foundation_homepage = WagtailHomepageFactory()
        self.mozfest_homepage = MozfestHomepageFactory()
        self.blog_page = BlogPageFactory()
        self.view_url = "/.well-known/apple-developer-merchantid-domain-association"

    def test_foundation_site_request(self):
        """
        Make sure the view returns the foundation specific key,
        when a request is made from the foundation site.
        """
        settings.APPLE_PAY_DOMAIN_ASSOCIATION_KEY_FOUNDATION = "test_foundation_key"
        self.site.root_page = self.foundation_homepage
        self.site.save()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "test_foundation_key")

    def test_foundation_site_request_with_no_key_set(self):
        """
        If no foundation site key is set, the view should return a
        'key not found' error message.
        """
        settings.APPLE_PAY_DOMAIN_ASSOCIATION_KEY_FOUNDATION = None
        self.site.root_page = self.foundation_homepage
        self.site.save()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 501)
        self.assertEqual(response.content.decode(), "Key not found. Please check environment variables.")

    def test_mozfest_site_request(self):
        """
        Make sure the view returns the mozfest specific key,
        when a request is made from the mozfest site.
        """
        settings.APPLE_PAY_DOMAIN_ASSOCIATION_KEY_MOZFEST = "test_mozfest_key"
        self.site.root_page = self.mozfest_homepage
        self.site.save()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "test_mozfest_key")

    def test_mozfest_site_request_with_no_key_set(self):
        """
        If no mozfest site key is set, the view should return a
        'key not found' error message.
        """
        settings.APPLE_PAY_DOMAIN_ASSOCIATION_KEY_MOZFEST = None
        self.site.root_page = self.foundation_homepage
        self.site.save()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 501)
        self.assertEqual(response.content.decode(), "Key not found. Please check environment variables.")

    def test_request_from_other_site(self):
        """
        Making sure that any request from a site that has neither a
        'WagtailHomePage' or a 'MozfestHomePage' set as the root,
        returns a 400 error.
        """
        self.site.root_page = self.blog_page
        self.site.save()

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Request site not recognized.")
