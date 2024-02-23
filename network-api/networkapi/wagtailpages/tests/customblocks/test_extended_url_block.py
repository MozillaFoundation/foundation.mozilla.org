from unittest import TestCase

from django.core import validators

from networkapi.wagtailpages.pagemodels.customblocks.extended_url_block import extended_url_validator


class TestExtendedUrlValidator(TestCase):
    def test_empty_string(self):
        """The function correctly handles an empty string."""
        url = ""
        with self.assertRaises(validators.ValidationError):
            extended_url_validator(url)

    def test_valid_mailto_url(self):
        """The function correctly validates a mailto URL."""
        url = "mailto:test@example.com"
        self.assertIsNone(extended_url_validator(url))

    def test_invalid_mailto_url(self):
        """The function correctly handles an invalid mailto URL."""
        url = "mailto:test"
        with self.assertRaises(validators.ValidationError):
            extended_url_validator(url)

    def test_valid_relative_url(self):
        """The function correctly validates a relative URL."""
        url = "/example"
        self.assertIsNone(extended_url_validator(url))
        url = "/example/"
        self.assertIsNone(extended_url_validator(url))
        url = "/example/path"

    def test_valid_relative_url_with_query_string(self):
        """The function correctly validates a relative URL with a query string."""
        url = "/example?query=string"
        self.assertIsNone(extended_url_validator(url))

    def test_invalid_relative_url(self):
        """The function correctly handles an invalid relative URL."""
        url = "/invalid path"
        with self.assertRaises(validators.ValidationError):
            extended_url_validator(url)

    def test_valid_absolute_url(self):
        """The function correctly validates an absolute URL."""
        url = "http://example.com"
        self.assertIsNone(extended_url_validator(url))

    def test_invalid_scheme(self):
        """The function correctly handles a URL with an invalid scheme."""
        url = "invalid://example.com"
        with self.assertRaises(validators.ValidationError):
            extended_url_validator(url)

    def test_invalid_domain_name(self):
        """The function correctly handles a URL with an invalid domain name."""
        url = "http://invalid_domain"
        with self.assertRaises(validators.ValidationError):
            extended_url_validator(url)

    def test_invalid_url_path(self):
        """The function correctly handles a URL with an invalid path."""
        url = "http://example.com/invalid path"
        with self.assertRaises(validators.ValidationError):
            extended_url_validator(url)

    def test_invalid_query_string(self):
        """The function correctly handles a URL with an invalid query string."""
        url = "http://example.com?invalid query"
        with self.assertRaises(validators.ValidationError):
            extended_url_validator(url)

    def test_invalid_fragment(self):
        """The function correctly handles a URL with an invalid fragment."""
        url = "http://example.com#invalid fragment"
        with self.assertRaises(validators.ValidationError):
            extended_url_validator(url)

    def test_invalid_port(self):
        """The function correctly handles a URL with an invalid port."""
        url = "http://example.com:invalid"
        with self.assertRaises(validators.ValidationError):
            extended_url_validator(url)

    def test_invalid_input_not_url_or_email(self):
        """The function correctly handles an invalid input that is neither a URL nor an email."""
        url = "invalid"
        with self.assertRaises(validators.ValidationError):
            extended_url_validator(url)
