from django.contrib.auth.models import User
from django.test import Client, TestCase
from wagtail.models import Page, Site


class SearchViewTestCase(TestCase):
    def setUp(self):
        # Set up the client for making requests
        self.client = Client()

        self.user = User.objects.create_superuser(username="admin", email="admin@example.com", password="password")

        # Log in as the superuser
        self.client.login(username="admin", password="password")

        # Create sample pages
        self.root_page = Page.get_first_root_node()
        site = Site.objects.get(is_default_site=True)

        self.page1 = self.root_page.add_child(instance=Page(title="Page One", slug="page-one"))

        # Add another child page under the root (depth=2)
        self.page2 = self.root_page.add_child(instance=Page(title="Page Two", slug="page-two"))
        site.save()

    def test_search_returns_multiple_pages(self):
        # Perform a search that should match multiple pages
        response = self.client.get("/cms/pages/search/", {"query": "Page"})

        # Confirm the response is successful
        self.assertEqual(response.status_code, 200)

        # Ensure both pages appear in the search results
        self.assertContains(response, "Page One")
        self.assertContains(response, "Page Two")
