from django.test import TestCase, Client
from wagtail.models import Page


class SearchViewTestCase(TestCase):
    def setUp(self):
        # Set up the client for making requests
        self.client = Client()

        # Create sample pages
        self.page1 = Page.objects.create(title="Page One", slug="page-one")
        self.page2 = Page.objects.create(title="Page Two", slug="page-two")

    def test_search_return_none(self):
        # Test the view when no query is provided
        response = self.client.get("/admin/pages/search/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, no pages match")

    def test_search_with_query(self):
        # Test the view when a valid query is provided
        response = self.client.get("/admin/pages/search/", {"query": "Page One"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Page One")

