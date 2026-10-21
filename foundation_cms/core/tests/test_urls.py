from django.test import TestCase
from django.urls import reverse
from django.utils import translation


class JavaScriptCatalogURLTests(TestCase):
    def test_catalog_url_carries_the_active_locale(self):
        with translation.override("fr"):
            self.assertEqual(reverse("javascript-catalog"), "/fr/jsi18n/")

        with translation.override("en"):
            self.assertEqual(reverse("javascript-catalog"), "/en/jsi18n/")

    def test_catalog_locale_comes_from_the_url_not_the_request(self):
        response = self.client.get("/fr/jsi18n/", headers={"accept-language": "en-US,en"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Language"], "fr")
