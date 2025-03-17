from django.test.utils import override_settings
from wagtail.contrib.redirects.models import Redirect

from foundation_cms.legacy_apps.wagtailpages.factory import (
    buyersguide as buyersguide_factories,
)
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base


# Safeguard against the fact that static assets and views might be hosted remotely,
# see https://docs.djangoproject.com/en/3.1/topics/testing/tools/#urlconf-configuration
@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class LocalizedRedirectTests(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.buyersguide_homepage = buyersguide_factories.BuyersGuidePageFactory(
            parent=cls.homepage,
        )
        cls.content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=cls.buyersguide_homepage,
        )

    def test_redirect(self):
        """Check that we are redirected to the localized version
        of the homepage when a Redirect object exists.
        In this example, a Redirect object exists for /test/ -> /
        so we expect to be redirected to /en/ when we visit /test/
        """
        redirect = Redirect(old_path="/test", redirect_link="/final")
        redirect.save()
        response = self.client.get("/test/", follow=True)

        self.assertEqual(response.redirect_chain, [("/final", 301), ("/en/final/", 302)])

        # Finally, check that the redirect doesn't work for other locales
        # since a redirect only exists for /test/ -> /final/
        response = self.client.get("/en/test/", follow=True)

        self.assertEqual(response.status_code, 404)

        response = self.client.get("/fr/test/", follow=True)

        self.assertEqual(response.status_code, 404)

    def test_localized_redirect(self):
        """Check that a Redirect with a language code in the old_path
        and no language code in the redirect_link is handled correctly.
        We expect to be redirected to /en/final/ when we visit /en/test/.
        """
        redirect = Redirect(old_path="/en/test", redirect_link="/final")
        redirect.save()
        response = self.client.get("/final/", follow=True)

        self.assertEqual(response.redirect_chain, [("/en/final/", 302)])

        response = self.client.get("/en/test/", follow=True)

        self.assertEqual(response.redirect_chain, [("/final", 301), ("/en/final/", 302)])

    def test_localized_redirect_to_default_locale(self):
        """Check that a Redirect with a language code in the old_path
        and no language code in the redirect_link is handled correctly.
        We expect /fr/test/ -> /final/ Should land at the default locale /en/final/
        """
        # First ensure no redirects exist that can intefere with this test
        self.assertFalse(Redirect.objects.all())

        redirect = Redirect(old_path="/fr/test", redirect_link="/final")
        redirect.save()
        response = self.client.get("/fr/test/", follow=True)

        self.assertEqual(response.redirect_chain, [("/final", 301), ("/en/final/", 302)])

    def test_fr_redirect_to_fr_target(self):
        """Check that a Redirect with a language code in the old_path
        and language code in the redirect_link is handled correctly.
        We expect /fr/test/ -> /fr/final/ Should land at /fr/final/
        """
        # First ensure no redirects exist that can intefere with this test
        self.assertFalse(Redirect.objects.all())

        redirect = Redirect(old_path="/fr/test", redirect_link="/fr/final")
        redirect.save()
        response = self.client.get("/fr/test/", follow=True)

        self.assertEqual(response.redirect_chain, [("/fr/final", 301), ("/fr/final/", 301)])

    def test_no_redirect_does_redirect(self):
        """Prove that a path is redirected to /en/ even if there isn't
        a Redirect object added. This is evidence that the localization
        framework is handling it.
        """
        response = self.client.get("/no-redirect/", follow=True)

        self.assertEqual(response.redirect_chain, [("/en/no-redirect/", 302)])
