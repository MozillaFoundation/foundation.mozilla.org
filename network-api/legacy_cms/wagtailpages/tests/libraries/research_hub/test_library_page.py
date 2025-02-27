import datetime
import os

from django.core import management, paginator
from django.utils import translation

from legacy_cms.wagtailpages.factory import profiles as profiles_factory
from legacy_cms.wagtailpages.factory.libraries.research_hub import (
    detail_page as detail_page_factory,
)
from legacy_cms.wagtailpages.factory.libraries.research_hub import (
    relations as relations_factory,
)
from legacy_cms.wagtailpages.factory.libraries.research_hub import (
    taxonomies as taxonomies_factory,
)
from legacy_cms.wagtailpages.pagemodels.libraries import constants
from legacy_cms.wagtailpages.pagemodels.libraries.research_hub.forms import (
    ResearchLibraryPageFilterForm,
)
from legacy_cms.wagtailpages.tests.libraries.research_hub import (
    base as research_test_base,
)
from legacy_cms.wagtailpages.tests.libraries.research_hub import (
    utils as research_test_utils,
)


class TestResearchLibraryPage(research_test_base.ResearchHubTestCase):
    def update_index(self):
        with open(os.devnull, "w") as f:
            management.call_command("update_index", verbosity=0, stdout=f)

    def test_get_research_detail_pages(self):
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )

        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages()

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)

    def test_get_research_detail_pages_with_translation_aliases(self):
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        self.synchronize_tree()
        fr_detail_page_1 = detail_page_1.get_translation(self.fr_locale)
        fr_detail_page_2 = detail_page_2.get_translation(self.fr_locale)

        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages()

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)
        self.assertNotIn(fr_detail_page_1, research_detail_pages)
        self.assertNotIn(fr_detail_page_2, research_detail_pages)

    def test_private_detail_pages_are_hidden(self):
        public_detail_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        private_detail_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        self.make_page_private(private_detail_page)

        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages()
        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(public_detail_page, research_detail_pages)
        self.assertNotIn(private_detail_page, research_detail_pages)

    def test_sort_newest_first(self):
        oldest_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2),
        )
        newest_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1),
        )

        research_detail_pages = list(
            self.library_page.get_sorted_filtered_detail_pages(sort=constants.SORT_NEWEST_FIRST)
        )

        newest_page_index = research_detail_pages.index(newest_page)
        oldest_page_index = research_detail_pages.index(oldest_page)
        self.assertLess(newest_page_index, oldest_page_index)

    def test_sort_oldest_first(self):
        oldest_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2),
        )
        newest_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1),
        )

        research_detail_pages = list(
            self.library_page.get_sorted_filtered_detail_pages(sort=constants.SORT_OLDEST_FIRST)
        )

        newest_page_index = research_detail_pages.index(newest_page)
        oldest_page_index = research_detail_pages.index(oldest_page)
        self.assertLess(oldest_page_index, newest_page_index)

    def test_sort_alphabetical(self):
        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Apple",
        )
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Banana",
        )

        research_detail_pages = list(
            self.library_page.get_sorted_filtered_detail_pages(sort=constants.SORT_ALPHABETICAL)
        )

        apple_page_index = research_detail_pages.index(apple_page)
        banana_page_index = research_detail_pages.index(banana_page)
        self.assertLess(apple_page_index, banana_page_index)

    def test_sort_alphabetical_reversed(self):
        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Apple",
        )
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Banana",
        )

        research_detail_pages = list(
            self.library_page.get_sorted_filtered_detail_pages(sort=constants.SORT_ALPHABETICAL_REVERSED)
        )

        apple_page_index = research_detail_pages.index(apple_page)
        banana_page_index = research_detail_pages.index(banana_page)
        self.assertLess(banana_page_index, apple_page_index)

    def test_get_research_detail_pages_sort_default(self):
        detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2),
        )
        detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1),
        )

        default_sort_detail_pages = list(self.library_page.get_sorted_filtered_detail_pages())
        newest_first_detail_pages = list(
            self.library_page.get_sorted_filtered_detail_pages(sort=constants.SORT_NEWEST_FIRST)
        )

        self.assertEqual(default_sort_detail_pages, newest_first_detail_pages)

    def test_pagination(self):
        self.library_page.results_count = 4
        self.library_page.save()
        for _ in range(6):
            detail_page_factory.ResearchDetailPageFactory(parent=self.library_page)

        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages()

        research_detail_pages_paginator = paginator.Paginator(
            object_list=research_detail_pages,
            per_page=self.library_page.results_count,
            allow_empty_first_page=True,
        )

        first_page_response = research_detail_pages_paginator.get_page(1)
        second_page_response = research_detail_pages_paginator.get_page(2)

        self.assertEqual(len(first_page_response), 4)
        self.assertEqual(len(second_page_response), 2)


class TestResearchLibraryPageSearch(TestResearchLibraryPage):
    def test_search_by_detail_page_title(self):
        # Fields other than title are empty to avoid accidental test failures due to
        # fake data generation.
        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Apple",
            introduction="",
            overview="",
            collaborators="",
        )
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Banana",
            introduction="",
            overview="",
            collaborators="",
        )

        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")
        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_search_by_detail_page_introduction(self):
        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="Apple",
            overview="",
            collaborators="",
        )
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="Banana",
            overview="",
            collaborators="",
        )

        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_search_by_detail_page_overview(self):
        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="",
            overview="Apple",
            collaborators="",
        )
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="",
            overview="Banana",
            collaborators="",
        )

        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_search_by_detail_page_collaborators(self):
        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="",
            overview="",
            collaborators="Apple",
        )
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="",
            overview="",
            collaborators="Banana",
        )

        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_search_by_detail_page_author_name(self):
        """Test detail page can be searched by author profile name."""
        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        apple_profile = profiles_factory.ProfileFactory(
            name="Apple",
            tagline="",
            introduction="",
        )
        relations_factory.ResearchAuthorRelationFactory(detail_page=apple_page, author_profile=apple_profile)
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        banana_profile = profiles_factory.ProfileFactory(
            name="Banana",
            tagline="",
            introduction="",
        )
        relations_factory.ResearchAuthorRelationFactory(detail_page=banana_page, author_profile=banana_profile)
        self.update_index()

        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_search_by_detail_page_topic_name(self):
        """Test detail page can be searched by topic name."""
        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        apple_topic = taxonomies_factory.ResearchTopicFactory(
            name="Apple",
            description="",
        )
        relations_factory.ResearchDetailPageResearchTopicRelationFactory(detail_page=apple_page, topic=apple_topic)
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        banana_topic = taxonomies_factory.ResearchTopicFactory(
            name="banana",
            description="",
        )
        relations_factory.ResearchDetailPageResearchTopicRelationFactory(detail_page=banana_page, topic=banana_topic)
        self.update_index()

        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_search_by_detail_page_region_name(self):
        """Test detail page can be searched by region name."""
        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        apple_region = taxonomies_factory.ResearchRegionFactory(name="Apple")
        relations_factory.ResearchDetailPageResearchRegionRelationFactory(detail_page=apple_page, region=apple_region)
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        banana_region = taxonomies_factory.ResearchRegionFactory(name="banana")
        relations_factory.ResearchDetailPageResearchRegionRelationFactory(
            detail_page=banana_page, region=banana_region
        )
        self.update_index()

        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)


class TestResearchLibraryPageFilters(TestResearchLibraryPage):
    def test_filter_author_profile(self):
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        author_profile = detail_page_1.authors.first().author_profile
        self.assertNotEqual(
            author_profile,
            detail_page_2.authors.first().author_profile,
        )

        filter_form = ResearchLibraryPageFilterForm(data={"authors": [author_profile.id]})
        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_filter_multiple_author_profiles(self):
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_a = detail_page_1.authors.first().author_profile
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_b = detail_page_2.authors.first().author_profile
        # Make author of first page also an author of the second page
        relations_factory.ResearchAuthorRelationFactory(
            detail_page=detail_page_2,
            author_profile=profile_a,
        )

        response = self.client.get(
            self.library_page.url,
            data={"authors": [profile_a.id, profile_b.id]},
        )

        # Only show the page where both profiles are authors
        research_detail_pages = response.context["detail_pages"]
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)

    def test_filter_localized_author_profile(self):
        """
        When filtering for a localized author profile, we also want to show pages
        associated with the default locale's profile. This is because after tree sync,
        pages are copied to the different locales, but related models are still the ones
        from the default locale.

        This test is setting up an aliased page and a translated page. The aliased page
        is not associated with the translated profile, but we still want to see it in
        the results.
        """
        profile = profiles_factory.ProfileFactory()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            authors__author_profile=profile,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            authors__author_profile=profile,
        )
        self.synchronize_tree()
        detail_page_1_fr = detail_page_1.get_translation(self.fr_locale)
        self.assertEqual(profile, detail_page_1_fr.authors.first().author_profile)
        detail_page_2_fr = research_test_utils.translate_detail_page(detail_page_2, self.fr_locale)
        profile_fr = detail_page_2_fr.authors.first().author_profile
        self.assertNotEqual(profile, profile_fr)
        self.assertEqual(profile.translation_key, profile_fr.translation_key)
        translation.activate(self.fr_locale.language_code)

        filter_form = ResearchLibraryPageFilterForm(data={"authors": [profile_fr.id]})
        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_1_fr, research_detail_pages)
        self.assertIn(detail_page_2_fr, research_detail_pages)
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_filter_topic(self):
        topic_A = taxonomies_factory.ResearchTopicFactory()
        detail_page_A = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic_A,
        )
        topic_B = taxonomies_factory.ResearchTopicFactory()
        detail_page_B = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic_B,
        )

        filter_form = ResearchLibraryPageFilterForm(data={"topics": [topic_A.id]})
        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_A, research_detail_pages)
        self.assertNotIn(detail_page_B, research_detail_pages)

    def test_filter_multiple_topics(self):
        topic_A = taxonomies_factory.ResearchTopicFactory()
        topic_B = taxonomies_factory.ResearchTopicFactory()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic_A,
        )
        relations_factory.ResearchDetailPageResearchTopicRelationFactory(detail_page=detail_page_1, topic=topic_B)
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic_A,
        )

        filter_form = ResearchLibraryPageFilterForm(data={"topics": [topic_A.id, topic_B.id]})
        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_filter_localized_topic(self):
        """
        When filtering for a localized topic, we also want to show pages
        associated with the default locale's topic. This is because after tree sync,
        pages are copied to the different locales, but related models are still the ones
        from the default locale.

        This test is setting up an aliased page and a translated page. The aliased page
        is not associated with the translated topic, but we still want to see it in
        the results.
        """
        topic = taxonomies_factory.ResearchTopicFactory()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic,
        )
        self.synchronize_tree()
        detail_page_1_fr = detail_page_1.get_translation(self.fr_locale)
        self.assertEqual(topic, detail_page_1_fr.related_topics.first().topic)
        detail_page_2_fr = research_test_utils.translate_detail_page(detail_page_2, self.fr_locale)
        topic_fr = detail_page_2_fr.related_topics.first().topic
        self.assertNotEqual(topic, topic_fr)
        self.assertEqual(topic.translation_key, topic_fr.translation_key)
        translation.activate(self.fr_locale.language_code)

        filter_form = ResearchLibraryPageFilterForm(data={"topics": [topic_fr.id]})
        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1_fr, research_detail_pages)
        self.assertIn(detail_page_2_fr, research_detail_pages)
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_filter_region(self):
        region_A = taxonomies_factory.ResearchRegionFactory()
        detail_page_A = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__region=region_A,
        )
        region_B = taxonomies_factory.ResearchRegionFactory()
        detail_page_B = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__region=region_B,
        )

        filter_form = ResearchLibraryPageFilterForm(data={"regions": [region_A.id]})
        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_A, research_detail_pages)
        self.assertNotIn(detail_page_B, research_detail_pages)

    def test_filter_multiple_regions(self):
        region_A = taxonomies_factory.ResearchRegionFactory()
        region_B = taxonomies_factory.ResearchRegionFactory()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__region=region_A,
        )
        relations_factory.ResearchDetailPageResearchRegionRelationFactory(detail_page=detail_page_1, region=region_B)
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__region=region_A,
        )

        filter_form = ResearchLibraryPageFilterForm(data={"regions": [region_A.id, region_B.id]})
        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_filter_localized_region(self):
        """
        When filtering for a localized region, we also want to show pages
        associated with the default locale's region. This is because after tree sync,
        pages are copied to the different locales, but related models are still the ones
        from the default locale.

        This test is setting up an aliased page and a translated page. The aliased page
        is not associated with the translated region, but we still want to see it in
        the results.
        """
        region = taxonomies_factory.ResearchRegionFactory()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__region=region,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__region=region,
        )
        self.synchronize_tree()
        detail_page_1_fr = detail_page_1.get_translation(self.fr_locale)
        self.assertEqual(region, detail_page_1_fr.related_regions.first().region)
        detail_page_2_fr = research_test_utils.translate_detail_page(detail_page_2, self.fr_locale)
        region_fr = detail_page_2_fr.related_regions.first().region
        self.assertNotEqual(region, region_fr)
        self.assertEqual(region.translation_key, region_fr.translation_key)
        translation.activate(self.fr_locale.language_code)

        filter_form = ResearchLibraryPageFilterForm(data={"regions": [region_fr.id]})
        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1_fr, research_detail_pages)
        self.assertIn(detail_page_2_fr, research_detail_pages)
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_filter_for_year(self):
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        year_1 = detail_page_1.original_publication_date.year
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=datetime.date(year_1 + 1, 6, 1),
        )

        filter_form = ResearchLibraryPageFilterForm(data={"year": year_1})
        research_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)
