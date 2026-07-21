from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import Client, TestCase
from wagtail.models import Page, Site

from foundation_cms.search.models import SearchEvent


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


class SearchLoggingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.root_page = Page.get_first_root_node()
        site = Site.objects.get(is_default_site=True)

        # Create sample pages to search for
        self.page1 = self.root_page.add_child(instance=Page(title="Page One", slug="page-one"))
        self.page2 = self.root_page.add_child(instance=Page(title="Page Two", slug="page-two"))

        site.save()

    @patch("wagtail.contrib.search_promotions.models.Query.add_hit")
    def test_logging_on_initial_search_only(self, mock_add_hit):
        # First search: should create SearchEvent and call add_hit
        response = self.client.get("/en/search/", {"query": "Page"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SearchEvent.objects.count(), 1)

        # add_hit should be called for the initial search
        mock_add_hit.assert_called_once()

        # Pagination: should not create SearchEvent or call add_hit again
        response = self.client.get("/en/search/", {"query": "Page", "page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SearchEvent.objects.count(), 1)

        # add_hit should not be called again on pagination
        mock_add_hit.assert_called_once()

    @patch("wagtail.contrib.search_promotions.models.Query.add_hit")
    def test_no_logging_on_pagination_only(self, mock_add_hit):
        # If only navigating to page=2 without a prior search, should not log
        response = self.client.get("/en/search/", {"query": "Page", "page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SearchEvent.objects.count(), 0)

        # add_hit should not be called since there was no initial search
        mock_add_hit.assert_not_called()

    @patch("wagtail.contrib.search_promotions.models.Query.add_hit")
    def test_no_logging_on_filter_preview(self, mock_add_hit):
        response = self.client.get(
            "/en/search/",
            {"query": "Page", "content_type": "research"},
            headers={"X-Search-Preview": "true"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(SearchEvent.objects.count(), 0)
        mock_add_hit.assert_not_called()

    @patch("foundation_cms.search.views.get_search_backend_for_locale")
    def test_single_page_results_show_page_count(self, mock_get_search_backend):
        result_page = self.root_page.add_child(
            instance=Page(title="Unique Search Result", slug="unique-search-result")
        )
        search_backend = Mock()
        search_backend.search.return_value = [result_page]
        mock_get_search_backend.return_value = (search_backend, "database")

        response = self.client.get("/en/search/", {"query": "Unique Search Result"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Page 1 of 1")

    @patch("foundation_cms.search.views.get_search_backend_for_locale")
    def test_filter_toggle_shows_applied_filter_count(self, mock_get_search_backend):
        search_backend = Mock()
        search_backend.search.return_value = []
        mock_get_search_backend.return_value = (search_backend, "database")

        cases = (
            ({"query": "Page"}, 0),
            ({"query": "Page", "content_type": "research"}, 1),
            ({"query": "Page", "topic": "privacy"}, 1),
            ({"query": "Page", "content_type": "research", "topic": "privacy"}, 2),
            ({"query": "Page", "sort": "newest"}, 0),
        )

        for params, expected_count in cases:
            with self.subTest(params=params):
                response = self.client.get("/en/search/", params)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.context["active_filter_count"], expected_count)
                if expected_count:
                    self.assertContains(response, f"Filter & Sort ({expected_count})")
                else:
                    self.assertNotContains(response, "Filter & Sort (")
