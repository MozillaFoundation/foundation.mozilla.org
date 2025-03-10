from django.test import TestCase

from foundation_cms.base.models import HomePage


class HomePageTestCase(TestCase):
    def setUp(self):
        self.home_page = HomePage()

    def test_get_absolute_url(self):
        self.assertEqual(self.home_page, "/en/")
