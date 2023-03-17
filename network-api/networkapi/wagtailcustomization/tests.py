from django.test import TestCase
from django.test.utils import override_settings
from wagtail.contrib.redirects.models import Redirect


# Safeguard against the fact that static assets and views might be hosted remotely,
# see https://docs.djangoproject.com/en/3.1/topics/testing/tools/#urlconf-configuration
@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class LocalizedRedirectTests(TestCase):
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

    def test_no_redirect_does_redirect(self):
        """Prove that a path is redirected to /en/ even if there isn't
        a Redirect object added. This is evidence that the localization
        framework is handling it.
        """
        response = self.client.get("/no-redirect/", follow=True)

        self.assertEqual(response.redirect_chain, [("/en/no-redirect/", 302)])
