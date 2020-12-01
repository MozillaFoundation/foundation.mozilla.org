from django.test import TestCase
from wagtail.contrib.redirects.models import Redirect
from django.test.utils import override_settings


# Safeguard against the fact that static assets and views might be hosted remotely,
# see https://docs.djangoproject.com/en/3.1/topics/testing/tools/#urlconf-configuration
@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class LocalizedRedirectTests(TestCase):
    def setUp(self):
        redirect = Redirect(old_path='/test', redirect_link='/')
        redirect.save()

    def test_plain_redirect(self):
        response = self.client.get('/test/', follow=True)
        self.assertEqual(response.redirect_chain, [('/', 301), ('/en/', 302)])

    def test_localized_redirect(self):
        response = self.client.get('/en/test/', follow=True)
        self.assertEqual(response.redirect_chain, [('/', 301), ('/en/', 302)])
