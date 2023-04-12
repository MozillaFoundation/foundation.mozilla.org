
import datetime
import os
import time
import unittest

from django.core import management, paginator
from django.utils import timezone, translation

from networkapi.wagtailpages.factory import profiles as profiles_factory
from networkapi.wagtailpages.factory.research_hub import (
    detail_page as detail_page_factory,
)
from networkapi.wagtailpages.factory.research_hub import relations as relations_factory
from networkapi.wagtailpages.factory.research_hub import (
    taxonomies as taxonomies_factory,
)
from networkapi.wagtailpages.pagemodels.research_hub import constants
from networkapi.wagtailpages.tests.research_hub import base as research_test_base
from networkapi.wagtailpages.tests.research_hub import utils as research_test_utils


class TestResearchLibraryPage(research_test_base.ResearchHubTestCase):
    def update_index(self):
        with open(os.devnull, "w") as f:
            management.call_command("update_index", verbosity=0, stdout=f)

    def test_get_research_detail_pages(self):
        start_time = time.time()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )

        research_detail_pages = self.library_page._get_research_detail_pages()

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_get_research_detail_pages: {execution_time} seconds")

    def test_get_research_detail_pages_with_translation_aliases(self):
        start_time = time.time()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        self.synchronize_tree()
        fr_detail_page_1 = detail_page_1.get_translation(self.fr_locale)
        fr_detail_page_2 = detail_page_2.get_translation(self.fr_locale)

        research_detail_pages = self.library_page._get_research_detail_pages()

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)
        self.assertNotIn(fr_detail_page_1, research_detail_pages)
        self.assertNotIn(fr_detail_page_2, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_detail_pages_in_context_with_translation_aliases: {execution_time} seconds")

    def test_private_detail_pages_are_hidden(self):
        start_time = time.time()
        public_detail_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        private_detail_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        self.make_page_private(private_detail_page)

        research_detail_pages = self.library_page._get_research_detail_pages()
        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(public_detail_page, research_detail_pages)
        self.assertNotIn(private_detail_page, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_private_detail_pages_not_in_context: {execution_time} seconds")

    def test_search_by_detail_page_title(self):
        start_time = time.time()
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

        research_detail_pages = self.library_page._get_research_detail_pages(search="Apple")
        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_search_by_detail_page_title: {execution_time} seconds")

    def test_search_by_detail_page_introduction(self):
        start_time = time.time()
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

        research_detail_pages = self.library_page._get_research_detail_pages(search="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_search_by_detail_page_introduction: {execution_time} seconds")

    def test_search_by_detail_page_overview(self):
        start_time = time.time()
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

        research_detail_pages = self.library_page._get_research_detail_pages(search="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_search_by_detail_page_overview: {execution_time} seconds")

    def test_search_by_detail_page_collaborators(self):
        start_time = time.time()
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

        research_detail_pages = self.library_page._get_research_detail_pages(search="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_search_by_detail_page_collaborators: {execution_time} seconds")

    def test_search_by_detail_page_author_name(self):
        """Test detail page can be searched by author profile name."""
        start_time = time.time()
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
        relations_factory.ResearchAuthorRelationFactory(research_detail_page=apple_page, author_profile=apple_profile)
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
        relations_factory.ResearchAuthorRelationFactory(
            research_detail_page=banana_page, author_profile=banana_profile
        )
        self.update_index()

        research_detail_pages = self.library_page._get_research_detail_pages(search="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_search_by_detail_page_author_name: {execution_time} seconds")

    def test_search_by_detail_page_topic_name(self):
        """Test detail page can be searched by topic name."""
        start_time = time.time()
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
        relations_factory.ResearchDetailPageResearchTopicRelationFactory(
            research_detail_page=apple_page, research_topic=apple_topic
        )
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
        relations_factory.ResearchDetailPageResearchTopicRelationFactory(
            research_detail_page=banana_page, research_topic=banana_topic
        )
        self.update_index()

        research_detail_pages = self.library_page._get_research_detail_pages(search="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_search_by_detail_page_topic_name: {execution_time} seconds")

    def test_search_by_detail_page_region_name(self):
        """Test detail page can be searched by region name."""
        start_time = time.time()
        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        apple_region = taxonomies_factory.ResearchRegionFactory(name="Apple")
        relations_factory.ResearchDetailPageResearchRegionRelationFactory(
            research_detail_page=apple_page, research_region=apple_region
        )
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        banana_region = taxonomies_factory.ResearchRegionFactory(name="banana")
        relations_factory.ResearchDetailPageResearchRegionRelationFactory(
            research_detail_page=banana_page, research_region=banana_region
        )
        self.update_index()

        research_detail_pages = self.library_page._get_research_detail_pages(search="Apple")

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_search_by_detail_page_region_name: {execution_time} seconds")

    def test_sort_newest_first(self):
        start_time = time.time()
        oldest_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2),
        )
        newest_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1),
        )

        research_detail_pages = list(self.library_page._get_research_detail_pages(sort=constants.SORT_NEWEST_FIRST))

        newest_page_index = research_detail_pages.index(newest_page)
        oldest_page_index = research_detail_pages.index(oldest_page)
        self.assertLess(newest_page_index, oldest_page_index)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_sort_newest_first: {execution_time} seconds")

    def test_sort_oldest_first(self):
        start_time = time.time()
        oldest_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2),
        )
        newest_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1),
        )

        research_detail_pages = list(self.library_page._get_research_detail_pages(sort=constants.SORT_OLDEST_FIRST))

        newest_page_index = research_detail_pages.index(newest_page)
        oldest_page_index = research_detail_pages.index(oldest_page)
        self.assertLess(oldest_page_index, newest_page_index)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_sort_oldest_first: {execution_time} seconds")

    def test_sort_alphabetical(self):
        start_time = time.time()

        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Apple",
        )
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Banana",
        )

        research_detail_pages = list(self.library_page._get_research_detail_pages(sort=constants.SORT_ALPHABETICAL))

        apple_page_index = research_detail_pages.index(apple_page)
        banana_page_index = research_detail_pages.index(banana_page)
        self.assertLess(apple_page_index, banana_page_index)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_sort_alphabetical: {execution_time} seconds")

    def test_sort_alphabetical_reversed(self):
        start_time = time.time()

        apple_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Apple",
        )
        banana_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title="Banana",
        )

        research_detail_pages = list(self.library_page._get_research_detail_pages(sort=constants.SORT_ALPHABETICAL_REVERSED))

        apple_page_index = research_detail_pages.index(apple_page)
        banana_page_index = research_detail_pages.index(banana_page)
        self.assertLess(banana_page_index, apple_page_index)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_sort_alphabetical_reversed: {execution_time} seconds")

    def test_get_research_detail_pages_sort_default(self):
        start_time = time.time()

        detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2),
        )
        detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1),
        )

        default_sort_detail_pages = list(self.library_page._get_research_detail_pages())
        newest_first_detail_pages = list(self.library_page._get_research_detail_pages(sort=constants.SORT_NEWEST_FIRST))

        self.assertEqual(default_sort_detail_pages, newest_first_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_get_research_detail_pages_sort_default: {execution_time} seconds")

    def test_research_author_profile_in_options(self):
        start_time = time.time()

        detail_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )

        author_options = self.library_page._get_author_options()
        author_option_values = [i["value"] for i in author_options]

        self.assertIn(
            detail_page.research_authors.first().author_profile.id,
            author_option_values,
        )
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_research_author_profile_in_options: {execution_time} seconds")

    def test_non_research_author_profile_not_in_options(self):
        start_time = time.time()
        profile = profiles_factory.ProfileFactory()

        author_options = self.library_page._get_author_options()
        author_option_values = [i["value"] for i in author_options]

        self.assertNotIn(
            profile.id,
            author_option_values,
        )

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_non_research_author_profile_not_in_options: {execution_time} seconds")

    def test_research_author_in_context_aliased_detail_page_fr(self):
        """
        After the treesync, there are alias pages in the non-default locales. But,
        before the pages are translated (a manual action) the related models like author
        are still the ones from the default locale.
        """
        start_time = time.time()

        detail_page_en = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_en = detail_page_en.research_authors.first().author_profile
        self.synchronize_tree()
        translation.activate(self.fr_locale.language_code)

        author_options = self.library_page.localized._get_author_options()
        author_option_values = [i["value"] for i in author_options]

        self.assertIn(
            profile_en.id,
            author_option_values,
        )
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_research_author_in_context_aliased_detail_page_fr: {execution_time} seconds")

    def test_research_author_in_context_translated_detail_page_fr(self):
        """
        When a profile for the active locale exists, pass that one to the context.

        Profiles are not necessarily people, so they might have translated names.
        """
        start_time = time.time()

        detail_page_en = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_en = detail_page_en.research_authors.first().author_profile
        self.synchronize_tree()
        detail_page_fr = research_test_utils.translate_detail_page(detail_page_en, self.fr_locale)
        profile_fr = detail_page_fr.research_authors.first().author_profile
        translation.activate(self.fr_locale.language_code)

        author_options = self.library_page.localized._get_author_options()
        author_option_values = [i["value"] for i in author_options]

        self.assertNotIn(
            profile_en.id,
            author_option_values,
        )
        self.assertIn(
            profile_fr.id,
            author_option_values,
        )
        end_time = time.time()
        execution_time = end_time - start_time
        print(
            f"Execution time for test_research_author_in_context_translated_detail_page_fr: {execution_time} seconds"
        )

    def test_filter_author_profile(self):
        start_time = time.time()

        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        author_profile = detail_page_1.research_authors.first().author_profile
        self.assertNotEqual(
            author_profile,
            detail_page_2.research_authors.first().author_profile,
        )

        research_detail_pages = self.library_page._get_research_detail_pages(author_profile_ids=[author_profile.id])

        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_filter_author_profile: {execution_time} seconds")

    def test_filter_multiple_author_profiles(self):
        start_time = time.time()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_a = detail_page_1.research_authors.first().author_profile
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_b = detail_page_2.research_authors.first().author_profile
        # Make author of first page also an author of the second page
        relations_factory.ResearchAuthorRelationFactory(
            research_detail_page=detail_page_2,
            author_profile=profile_a,
        )

        response = self.client.get(
            self.library_page.url,
            data={"author": [profile_a.id, profile_b.id]},
        )

        # Only show the page where both profiles are authors
        research_detail_pages = response.context["research_detail_pages"]
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_filter_multiple_author_profiles: {execution_time} seconds")

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
        start_time = time.time()

        profile = profiles_factory.ProfileFactory()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            research_authors__author_profile=profile,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            research_authors__author_profile=profile,
        )
        self.synchronize_tree()
        detail_page_1_fr = detail_page_1.get_translation(self.fr_locale)
        self.assertEqual(profile, detail_page_1_fr.research_authors.first().author_profile)
        detail_page_2_fr = research_test_utils.translate_detail_page(detail_page_2, self.fr_locale)
        profile_fr = detail_page_2_fr.research_authors.first().author_profile
        self.assertNotEqual(profile, profile_fr)
        self.assertEqual(profile.translation_key, profile_fr.translation_key)
        translation.activate(self.fr_locale.language_code)

        research_detail_pages = self.library_page.localized._get_research_detail_pages(author_profile_ids=[profile_fr.id])


        self.assertIn(detail_page_1_fr, research_detail_pages)
        self.assertIn(detail_page_2_fr, research_detail_pages)
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_filter_localized_author_profile: {execution_time} seconds")

    def test_research_topics_in_options(self):
        start_time = time.time()
        topic_1 = taxonomies_factory.ResearchTopicFactory()
        topic_2 = taxonomies_factory.ResearchTopicFactory()

        topic_options = self.library_page._get_topic_options()
        topic_option_values = [i["value"] for i in topic_options]

        self.assertEqual(len(topic_option_values), 2)
        self.assertIn(topic_1.id, topic_option_values)
        self.assertIn(topic_2.id, topic_option_values)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_research_topics_in_options: {execution_time} seconds")

    def test_topic_in_options_matches_active_locale(self):
        start_time = time.time()

        topic_en = taxonomies_factory.ResearchTopicFactory()
        topic_fr = topic_en.copy_for_translation(self.fr_locale)
        topic_fr.save()

        topic_options_en = self.library_page.localized._get_topic_options()
        topic_option_values_en = [i["value"] for i in topic_options_en]

        translation.activate(self.fr_locale.language_code)

        topic_options_fr = self.library_page.localized._get_topic_options()
        topic_option_values_fr = [i["value"] for i in topic_options_fr]

        self.assertEqual(len(topic_option_values_en), 1)
        self.assertIn(topic_en.id, topic_option_values_en)
        self.assertNotIn(topic_fr.id, topic_option_values_en)
        self.assertEqual(len(topic_option_values_fr), 1)
        self.assertNotIn(topic_en.id, topic_option_values_fr)
        self.assertIn(topic_fr.id, topic_option_values_fr)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_topic_in_options_matches_active_locale: {execution_time} seconds")

    def test_localized_topic_options(self):
        """
        Use active locales version of topic if available.

        If no translation is available for a given topic, display the default locale
        topic.

        """
        start_time = time.time()
        topic_1_en = taxonomies_factory.ResearchTopicFactory()
        topic_1_fr = topic_1_en.copy_for_translation(self.fr_locale)
        topic_1_fr.save()
        topic_2_en = taxonomies_factory.ResearchTopicFactory()
        translation.activate(self.fr_locale.language_code)

        topic_options = self.library_page.localized._get_topic_options()
        topic_option_values = [i["value"] for i in topic_options]

        self.assertEqual(len(topic_option_values), 2)
        self.assertNotIn(topic_1_en.id, topic_option_values)
        self.assertIn(topic_1_fr.id, topic_option_values)
        self.assertIn(topic_2_en.id, topic_option_values)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_localized_topic_options: {execution_time} seconds")

    def test_filter_topic(self):
        start_time = time.time()

        topic_A = taxonomies_factory.ResearchTopicFactory()
        detail_page_A = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__research_topic=topic_A,
        )
        topic_B = taxonomies_factory.ResearchTopicFactory()
        detail_page_B = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__research_topic=topic_B,
        )

        research_detail_pages = self.library_page._get_research_detail_pages(topic_ids=[topic_A.id])

        self.assertIn(detail_page_A, research_detail_pages)
        self.assertNotIn(detail_page_B, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_filter_topic: {execution_time} seconds")

    def test_filter_multiple_topics(self):
        start_time = time.time()

        topic_A = taxonomies_factory.ResearchTopicFactory()
        topic_B = taxonomies_factory.ResearchTopicFactory()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__research_topic=topic_A,
        )
        relations_factory.ResearchDetailPageResearchTopicRelationFactory(
            research_detail_page=detail_page_1, research_topic=topic_B
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__research_topic=topic_A,
        )

        research_detail_pages = self.library_page._get_research_detail_pages(topic_ids=[topic_A.id, topic_B.id])

        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_filter_multiple_topics: {execution_time} seconds")

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
        start_time = time.time()

        topic = taxonomies_factory.ResearchTopicFactory()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__research_topic=topic,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__research_topic=topic,
        )
        self.synchronize_tree()
        detail_page_1_fr = detail_page_1.get_translation(self.fr_locale)
        self.assertEqual(topic, detail_page_1_fr.related_topics.first().research_topic)
        detail_page_2_fr = research_test_utils.translate_detail_page(detail_page_2, self.fr_locale)
        topic_fr = detail_page_2_fr.related_topics.first().research_topic
        self.assertNotEqual(topic, topic_fr)
        self.assertEqual(topic.translation_key, topic_fr.translation_key)
        translation.activate(self.fr_locale.language_code)

        research_detail_pages = self.library_page.localized._get_research_detail_pages(topic_ids=[topic_fr.id])

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1_fr, research_detail_pages)
        self.assertIn(detail_page_2_fr, research_detail_pages)
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_filter_localized_topic: {execution_time} seconds")

    def test_research_regions_in_options(self):
        start_time = time.time()

        region_1 = taxonomies_factory.ResearchRegionFactory()
        region_2 = taxonomies_factory.ResearchRegionFactory()

        response = self.client.get(self.library_page.url)

        region_option_values = [i["value"] for i in response.context["region_options"]]
        self.assertEqual(len(region_option_values), 2)
        self.assertIn(region_1.id, region_option_values)
        self.assertIn(region_2.id, region_option_values)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_research_regions_in_options: {execution_time} seconds")

    def test_region_in_options_matches_active_locale(self):
        start_time = time.time()
        region_en = taxonomies_factory.ResearchRegionFactory()
        region_fr = region_en.copy_for_translation(self.fr_locale)
        region_fr.save()

        response_en = self.client.get(self.library_page.localized.url)
        translation.activate(self.fr_locale.language_code)
        response_fr = self.client.get(self.library_page.localized.url)

        region_option_values_en = [i["value"] for i in response_en.context["region_options"]]
        self.assertEqual(len(region_option_values_en), 1)
        self.assertIn(region_en.id, region_option_values_en)
        self.assertNotIn(region_fr.id, region_option_values_en)
        region_option_values_fr = [i["value"] for i in response_fr.context["region_options"]]
        self.assertEqual(len(region_option_values_fr), 1)
        self.assertNotIn(region_en.id, region_option_values_fr)
        self.assertIn(region_fr.id, region_option_values_fr)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_region_in_options_matches_active_locale: {execution_time} seconds")

    def test_localized_region_options(self):
        """
        Use active locales version of region if available.

        If no translation is available for a given region, display the default locale
        region.

        """
        start_time = time.time()

        region_1_en = taxonomies_factory.ResearchRegionFactory()
        region_1_fr = region_1_en.copy_for_translation(self.fr_locale)
        region_1_fr.save()
        region_2_en = taxonomies_factory.ResearchRegionFactory()
        translation.activate(self.fr_locale.language_code)

        response = self.client.get(self.library_page.localized.url)

        region_option_values = [i["value"] for i in response.context["region_options"]]
        self.assertEqual(len(region_option_values), 2)
        self.assertNotIn(region_1_en.id, region_option_values)
        self.assertIn(region_1_fr.id, region_option_values)
        self.assertIn(region_2_en.id, region_option_values)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_localized_region_options: {execution_time} seconds")

    def test_filter_region(self):
        start_time = time.time()
        region_A = taxonomies_factory.ResearchRegionFactory()
        detail_page_A = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__research_region=region_A,
        )
        region_B = taxonomies_factory.ResearchRegionFactory()
        detail_page_B = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__research_region=region_B,
        )

        response = self.client.get(self.library_page.url, data={"region": region_A.id})

        research_detail_pages = response.context["research_detail_pages"]
        self.assertIn(detail_page_A, research_detail_pages)
        self.assertNotIn(detail_page_B, research_detail_pages)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_filter_region: {execution_time} seconds")

    def test_filter_multiple_regions(self):
        start_time = time.time()

        region_A = taxonomies_factory.ResearchRegionFactory()
        region_B = taxonomies_factory.ResearchRegionFactory()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__research_region=region_A,
        )
        relations_factory.ResearchDetailPageResearchRegionRelationFactory(
            research_detail_page=detail_page_1, research_region=region_B
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__research_region=region_A,
        )

        response = self.client.get(self.library_page.url, data={"region": [region_A.id, region_B.id]})

        research_detail_pages = response.context["research_detail_pages"]
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_filter_multiple_regions: {execution_time} seconds")

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
        start_time = time.time()

        region = taxonomies_factory.ResearchRegionFactory()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__research_region=region,
        )
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__research_region=region,
        )
        self.synchronize_tree()
        detail_page_1_fr = detail_page_1.get_translation(self.fr_locale)
        self.assertEqual(region, detail_page_1_fr.related_regions.first().research_region)
        detail_page_2_fr = research_test_utils.translate_detail_page(detail_page_2, self.fr_locale)
        region_fr = detail_page_2_fr.related_regions.first().research_region
        self.assertNotEqual(region, region_fr)
        self.assertEqual(region.translation_key, region_fr.translation_key)
        translation.activate(self.fr_locale.language_code)

        response = self.client.get(
            self.library_page.localized.url,
            data={"region": region_fr.id},
        )

        research_detail_pages = response.context["research_detail_pages"]
        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1_fr, research_detail_pages)
        self.assertIn(detail_page_2_fr, research_detail_pages)
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_filter_localized_region: {execution_time} seconds")

    def test_years_in_options(self):
        start_time = time.time()
        year_1 = timezone.now().year
        year_2 = year_1 - 1
        detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=datetime.date(year=year_1, month=1, day=1),
        )
        detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=datetime.date(year=year_2, month=1, day=1),
        )

        response = self.client.get(self.library_page.url)

        year_option_values = [i["value"] for i in response.context["year_options"]]
        # It's 3 options because of the two years and the "any" option.
        self.assertEqual(len(year_option_values), 3)
        self.assertIn(year_1, year_option_values)
        self.assertIn(year_2, year_option_values)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_years_in_options: {execution_time} seconds")

    def test_filter_for_year(self):
        start_time = time.time()
        detail_page_1 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        year_1 = detail_page_1.original_publication_date.year
        detail_page_2 = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=datetime.date(year_1 + 1, 6, 1),
        )

        response = self.client.get(self.library_page.url, data={"year": year_1})

        research_detail_pages = response.context["research_detail_pages"]
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_filter_for_year: {execution_time} seconds")

    def test_library_page_breadcrumbs(self):
        start_time = time.time()
        response = self.client.get(self.library_page.url)
        breadcrumbs = response.context["breadcrumbs"]
        expected_breadcrumbs = [{"title": "Research", "url": "/en/research/"}]

        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_library_page_breadcrumbs: {execution_time} seconds")

    def test_pagination(self):
        start_time = time.time()

        self.library_page.results_count = 4
        self.library_page.save()
        for _ in range(6):
            detail_page_factory.ResearchDetailPageFactory(parent=self.library_page)

        first_page_response = self.client.get(self.library_page.url, data={"page": 1})
        second_page_response = self.client.get(self.library_page.url, data={"page": 2})

        first_page_detail_pages = first_page_response.context["research_detail_pages"]
        self.assertEqual(len(first_page_detail_pages), 4)
        second_page_detail_pages = second_page_response.context["research_detail_pages"]
        self.assertEqual(len(second_page_detail_pages), 2)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for test_pagination: {execution_time} seconds")

