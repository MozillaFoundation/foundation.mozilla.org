from unittest import TestCase

from faker import Faker

from foundation_cms.legacy_apps.wagtailpages.templatetags import mini_site_tags


class GenerateThankYouURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake = Faker()

    def test_url(self):
        url = self.fake.url()
        thank_you_url = mini_site_tags._generate_thank_you_url(url)
        self.assertEqual(thank_you_url, f"{url}?thank_you=true")

    def test_url_keeps_query_params(self):
        url = f"{self.fake.url()}?test=123&testa=123"
        thank_you_url = mini_site_tags._generate_thank_you_url(url)
        self.assertEqual(thank_you_url, f"{url}&thank_you=true")

    def test_url_keeps_utm_params(self):
        url = f"{self.fake.url()}?utm_source=source&utm_medium=medium"
        thank_you_url = mini_site_tags._generate_thank_you_url(url)
        self.assertEqual(thank_you_url, f"{url}&thank_you=true")

    def test_url_keeps_anchor(self):
        base_url = self.fake.url()
        url = f"{base_url}#test"
        thank_you_url = mini_site_tags._generate_thank_you_url(url)
        self.assertEqual(thank_you_url, f"{base_url}?thank_you=true#test")

    def test_url_keeps_query_params_and_anchor(self):
        base_url = self.fake.url()
        url = f"{base_url}?test=123&testa=123#test"
        thank_you_url = mini_site_tags._generate_thank_you_url(url)
        self.assertEqual(thank_you_url, f"{base_url}?test=123&testa=123&thank_you=true#test")
