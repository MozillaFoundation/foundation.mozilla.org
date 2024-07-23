from unittest import TestCase

from django.core.exceptions import ValidationError
from faker import Faker

from networkapi.wagtailpages import validators


class RelativeURLValidatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake = Faker()
        cls.validator = validators.RelativeURLValidator()

    def test_relative_url(self):
        """Assert that a relative URL is valid."""
        valid_examples = [
            "/test/",
            "/test/test/",
            "/test/123/",
            "/test?test=123",
            "/test?testa=123&testb=123",
            "/test#test",
            "/test#testa-testb",
            "/test/test?test=123&testa=123#test",
            "?test=123",
            "?testa=123&testb=123",
            "?test_a=123&test_b=123",
            "/" + self.fake.uri_path(),
        ]
        for idx, url in enumerate(valid_examples):
            with self.subTest(i=idx):
                self.assertIsNone(self.validator(url))

    def test_absolute_url(self):
        """Assert that an absolute URL is invalid."""
        url = "https://example.com/test/"
        with self.assertRaises(ValidationError):
            self.validator(url)
        url = self.fake.url()
        with self.assertRaises(ValidationError):
            self.validator(url)

    def test_anchor_url(self):
        """Assert that an anchor URL is invalid."""
        url = "#an-id"
        with self.assertRaises(ValidationError):
            self.validator(url)

    def test_relative_url_does_not_start_with_forward_slash(self):
        """Assert that relative URL must start with a forward slash or question mark."""
        url = "test/"
        with self.assertRaises(ValidationError):
            self.validator(url)

    def test_relative_url_starts_with_question_mark(self):
        """Assert that relative URL can start with a question mark."""
        url = "?foo=bar"
        try:
            self.validator(url)
        except ValidationError:
            self.fail(f"ValidationError was raised for a valid relative URL: {url}")

    def test_empty_url(self):
        """Assert that an empty URL is invalid."""
        url = ""
        with self.assertRaises(ValidationError):
            self.validator(url)

    def test_none_url(self):
        """Assert that a None URL is invalid."""
        url = None
        with self.assertRaises(ValidationError):
            self.validator(url)


class AnchorLinkValidatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake = Faker()
        cls.validator = validators.AnchorLinkValidator()

    def test_valid_anchor_link(self):
        valid_examples = [
            "#test",
            "#test-test",
            "#" + self.fake.slug(),
        ]
        for idx, url in enumerate(valid_examples):
            with self.subTest(i=idx):
                self.assertIsNone(self.validator(url))

    def test_absolute_url(self):
        """Assert that an absolute URL is invalid."""
        url = "https://example.com/test/"
        with self.assertRaises(ValidationError):
            self.validator(url)
        url = self.fake.url()
        with self.assertRaises(ValidationError):
            self.validator(url)

    def test_relative_url(self):
        """Assert that a relative URL is invalid."""
        url = "/test"
        with self.assertRaises(ValidationError):
            self.validator(url)

    def test_anchor_link_must_start_with_hash(self):
        """Assert that anchor link must start with a #."""
        url = "test-id"
        with self.assertRaises(ValidationError):
            self.validator(url)

    def test_empty_url(self):
        """Assert that an empty URL is invalid."""
        url = ""
        with self.assertRaises(ValidationError):
            self.validator(url)

    def test_none_url(self):
        """Assert that a None URL is invalid."""
        url = None
        with self.assertRaises(ValidationError):
            self.validator(url)
