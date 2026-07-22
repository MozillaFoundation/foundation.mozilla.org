from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from wagtail.models import Page

from foundation_cms.core.models import GeneralPage

TEST_KEYWORD = "SEARCH_COMMAND_TEST"


class LoadSearchTestDataTests(TestCase):
    def generated_pages(self):
        return GeneralPage.objects.filter(title__startswith=f"{TEST_KEYWORD} ")

    def run_command(self, **options):
        output = StringIO()
        call_command("load_search_test_data", keyword=TEST_KEYWORD, stdout=output, **options)
        return output.getvalue()

    def test_creates_searchable_pages_across_sections(self):
        output = self.run_command(count=8)

        pages = list(self.generated_pages().order_by("id"))
        self.assertEqual(len(pages), 8)
        self.assertTrue(all(page.live for page in pages))
        self.assertTrue(all(page.first_published_at for page in pages))
        self.assertEqual(
            {page.get_parent().slug for page in pages},
            {"what-we-do", "research", "press-release", "event"},
        )
        self.assertTrue(all(page.topic_relations.exists() for page in pages))
        self.assertIn("Created and published 8 search test pages", output)

        response = self.client.get("/en/search/", {"query": TEST_KEYWORD})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_search_results"], 8)

        response = self.client.get(
            "/en/search/",
            {"query": TEST_KEYWORD, "content_type": "research"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_search_results"], 2)

    def test_rerun_replaces_generated_pages(self):
        self.run_command(count=8)
        first_ids = set(self.generated_pages().values_list("id", flat=True))

        output = self.run_command(count=4)

        second_ids = set(self.generated_pages().values_list("id", flat=True))
        self.assertEqual(len(second_ids), 4)
        self.assertTrue(first_ids.isdisjoint(second_ids))
        self.assertIn("Replacing 8 existing search test pages", output)

    def test_delete_removes_only_generated_pages(self):
        retained_page = Page.get_first_root_node().add_child(
            instance=Page(title="Retained Page", slug="retained-page")
        )
        self.run_command(count=4)

        output = self.run_command(count=4, delete=True)

        self.assertFalse(self.generated_pages().exists())
        self.assertTrue(Page.objects.filter(pk=retained_page.pk).exists())
        self.assertIn("Deleted 4 generated search test pages", output)
