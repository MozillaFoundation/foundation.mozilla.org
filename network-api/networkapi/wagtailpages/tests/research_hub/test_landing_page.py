import datetime

from django.utils import timezone
from wagtail import models as wagtail_models

from networkapi.wagtailpages.factory.research_hub import detail_page as detail_page_factory
from networkapi.wagtailpages.tests.research_hub import base


class ResearchLandingPageTestCase(base.ResearchHubTestCase):
    def create_research_detail_page(self, days_ago=0):
        publication_date = timezone.now().date() - datetime.timedelta(days=days_ago)
        return detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=publication_date,
        )

    def test_get_latest_research_pages_returns_three_latest_pages_by_publication_date(self):
        """
        Ensure that the latest research pages are returned
        """
        detail_page_1 = self.create_research_detail_page(days_ago=4)
        detail_page_2 = self.create_research_detail_page(days_ago=3)
        detail_page_3 = self.create_research_detail_page(days_ago=2)
        detail_page_4 = self.create_research_detail_page(days_ago=1)

        latest_research_pages = self.landing_page.get_latest_research_pages()

        self.assertEqual(len(latest_research_pages), 3)
        self.assertIn(detail_page_4, latest_research_pages)
        self.assertIn(detail_page_3, latest_research_pages)
        self.assertIn(detail_page_2, latest_research_pages)
        self.assertNotIn(detail_page_1, latest_research_pages)

    def test_get_latest_research_pages_does_not_return_private_page(self):
        """
        Ensure that the latest research pages don't contain private pages.
        """
        detail_page_public = self.create_research_detail_page()
        detail_page_private = self.create_research_detail_page()
        wagtail_models.PageViewRestriction.objects.create(
            page=detail_page_private,
            restriction_type=wagtail_models.PageViewRestriction.PASSWORD,
            password="test",
        )

        latest_research_pages = self.landing_page.get_latest_research_pages()

        self.assertEqual(len(latest_research_pages), 1)
        self.assertIn(detail_page_public, latest_research_pages)
        self.assertNotIn(detail_page_private, latest_research_pages)
