from django.test import RequestFactory, TestCase
from wagtail.models import Site
from wagtail_factories import SiteFactory

from foundation_cms.legacy_apps.utility.redirects import redirect_to_default_cms_site


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

    def tearDown(self):
        # Re-instate localhost as the default site
        self.original_default_site.is_default_site = True
        self.original_default_site.save()

        # Remove the Site Factories
        self.default_site.delete()
        self.secondary_site.delete()
