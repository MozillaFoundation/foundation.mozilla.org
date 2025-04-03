from django.test import TestCase

from foundation_cms.core import factories


class HomePageTestCase(TestCase):
    def setUp(self):
        self.home_page = factories.create_homepage()

    def test_get_absolute_url(self):
        self.assertEqual(self.home_page.url, "/en/")
