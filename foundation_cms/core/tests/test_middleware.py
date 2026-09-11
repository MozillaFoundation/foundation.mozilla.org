from unittest.mock import MagicMock

from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from wagtail.models import Locale

from foundation_cms.core.middleware import PreferredLocaleRedirectMiddleware


@override_settings(
    LANGUAGE_CODE="en",
    LANGUAGE_COOKIE_NAME="django_language",
    LANGUAGES=(
        ("en", "English"),
        ("fr", "French"),
    ),
)
class PreferredLocaleRedirectMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.get_response = MagicMock(return_value=HttpResponse("ok"))
        self.middleware = PreferredLocaleRedirectMiddleware(self.get_response)

        Locale.objects.get_or_create(language_code="en")
        Locale.objects.get_or_create(language_code="fr")

    def request(self, path, method="get", language="fr"):
        request = getattr(self.factory, method)(path)
        request.COOKIES["django_language"] = language
        return request

    def test_redirects_non_localized_url_using_language_cookie(self):
        response = self.middleware(self.request("/what-we-do/inspire/?source=footer"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/fr/what-we-do/inspire/?source=footer")
        self.get_response.assert_not_called()

    def test_keeps_default_language_behavior(self):
        response = self.middleware(self.request("/what-we-do/inspire/", language="en"))

        self.assertEqual(response.status_code, 200)
        self.get_response.assert_called_once()

    def test_does_not_redirect_localized_url(self):
        response = self.middleware(self.request("/fr/what-we-do/inspire/", language="en"))

        self.assertEqual(response.status_code, 200)
        self.get_response.assert_called_once()

    def test_does_not_redirect_without_valid_cookie(self):
        response = self.middleware(self.request("/what-we-do/inspire/", language="xx"))

        self.assertEqual(response.status_code, 200)
        self.get_response.assert_called_once()

    def test_does_not_redirect_excluded_paths(self):
        for path in ("/api/news/", "/documents/", "/jsi18n/"):
            with self.subTest(path=path):
                self.get_response.reset_mock()

                response = self.middleware(self.request(path))

                self.assertEqual(response.status_code, 200)
                self.get_response.assert_called_once()

    def test_does_not_redirect_non_get_requests(self):
        response = self.middleware(self.request("/what-we-do/inspire/", method="post"))

        self.assertEqual(response.status_code, 200)
        self.get_response.assert_called_once()
