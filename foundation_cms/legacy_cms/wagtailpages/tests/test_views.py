from django.test import RequestFactory, SimpleTestCase

from foundation_cms.legacy_cms.wagtailpages.views import localized_redirect


class LocalizedRedirectTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_redirect_with_subpath_and_query_string(self):
        # Create a mock request object
        request = self.factory.get("/destination/")
        request.LANGUAGE_CODE = "en"
        request.META = {"QUERY_STRING": "param=value"}

        # Call the localized_redirect function
        result = localized_redirect(request, "subpath", "destination")

        # Assert that the redirect URL is correct
        self.assertEqual(result.url, "/en/destination/subpath?param=value")

    def test_redirect_with_empty_subpath_and_query_string(self):
        # Create a mock request object
        request = self.factory.get("/destination/")
        request.LANGUAGE_CODE = "en"
        request.META = {"QUERY_STRING": ""}

        # Call the localized_redirect function
        result = localized_redirect(request, "", "destination")

        # Assert that the redirect URL is correct
        self.assertEqual(result.url, "/en/destination/")

    def test_redirect_with_active_language(self):
        # Create a mock request object
        request = self.factory.get("/en/destination/")
        request.LANGUAGE_CODE = "fr"
        request.META = {"QUERY_STRING": ""}

        # Call the localized_redirect function
        result = localized_redirect(request, "", "destination")

        # Assert that the redirect URL is correct
        self.assertEqual(result.url, "/fr/destination/")
