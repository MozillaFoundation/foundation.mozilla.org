import datetime
import os
import unittest

from django.utils import translation
from django.core import management

from networkapi.wagtailpages.factory import profiles as profiles_factory
from networkapi.wagtailpages.factory import research_hub as research_factory
from networkapi.wagtailpages.tests.research_hub import base as research_test_base
from networkapi.wagtailpages.tests.research_hub import utils as research_test_utils


class TestResearchLibraryPage(research_test_base.ResearchHubTestCase):
    def update_index(self):
        with open(os.devnull, 'w') as f:
            management.call_command('update_index', verbosity=0, stdout=f)

    def test_detail_pages_in_context(self):
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )

        response = self.client.get(self.library_page.url)

        research_detail_pages = response.context['research_detail_pages']
        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)

    def test_detail_pages_in_context_with_translation_aliases(self):
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        self.synchronize_tree()
        fr_detail_page_1 = detail_page_1.get_translation(self.fr_locale)
        fr_detail_page_2 = detail_page_2.get_translation(self.fr_locale)

        response = self.client.get(self.library_page.url)

        research_detail_pages = response.context['research_detail_pages']
        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)
        self.assertNotIn(fr_detail_page_1, research_detail_pages)
        self.assertNotIn(fr_detail_page_2, research_detail_pages)

    def test_search_by_detail_page_title(self):
        # Fields other than title are empty to avoid accidental test failures due to
        # fake data generation.
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Apple',
            introduction='',
            overview='',
            collaborators='',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Banana',
            introduction='',
            overview='',
            collaborators='',
        )

        response = self.client.get(self.library_page.url, data={'search': 'Apple'})

        research_detail_pages = response.context['research_detail_pages']
        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_search_by_detail_page_introduction(self):
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Cherry',
            introduction='Apple',
            overview='',
            collaborators='',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Also cherry',
            introduction='Banana',
            overview='',
            collaborators='',
        )

        response = self.client.get(self.library_page.url, data={'search': 'Apple'})

        research_detail_pages = response.context['research_detail_pages']
        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_search_by_detail_page_overview(self):
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Cherry',
            introduction='',
            overview='Apple',
            collaborators='',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Also cherry',
            introduction='',
            overview='Banana',
            collaborators='',
        )

        response = self.client.get(self.library_page.url, data={'search': 'Apple'})

        research_detail_pages = response.context['research_detail_pages']
        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_search_by_detail_page_collaborators(self):
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Cherry',
            introduction='',
            overview='',
            collaborators='Apple',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Also cherry',
            introduction='',
            overview='',
            collaborators='Banana',
        )

        response = self.client.get(self.library_page.url, data={'search': 'Apple'})

        research_detail_pages = response.context['research_detail_pages']
        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_search_by_detail_page_author_name(self):
        '''Test detail page can be searched by author profile name.'''
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Cherry',
            introduction='',
            overview='',
            collaborators='',
        )
        apple_profile = profiles_factory.ProfileFactory(
            name='Apple',
            tagline='',
            introduction='',
        )
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=apple_page,
            author_profile=apple_profile
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Also cherry',
            introduction='',
            overview='',
            collaborators='',
        )
        banana_profile = profiles_factory.ProfileFactory(
            name='Banana',
            tagline='',
            introduction='',
        )
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=banana_page,
            author_profile=banana_profile
        )
        self.update_index()

        response = self.client.get(self.library_page.url, data={'search': 'Apple'})

        research_detail_pages = response.context['research_detail_pages']
        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_sort_newest_first(self):
        oldest_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2)
        )
        newest_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1)
        )

        response = self.client.get(
            self.library_page.url,
            data={'sort': self.library_page.SORT_NEWEST_FIRST.value}
        )

        research_detail_pages = list(response.context['research_detail_pages'])
        newest_page_index = research_detail_pages.index(newest_page)
        oldest_page_index = research_detail_pages.index(oldest_page)
        self.assertLess(newest_page_index, oldest_page_index)

    def test_sort_oldest_first(self):
        oldest_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2)
        )
        newest_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1)
        )

        response = self.client.get(
            self.library_page.url,
            data={'sort': self.library_page.SORT_OLDEST_FIRST.value}
        )

        research_detail_pages = list(response.context['research_detail_pages'])
        newest_page_index = research_detail_pages.index(newest_page)
        oldest_page_index = research_detail_pages.index(oldest_page)
        self.assertLess(oldest_page_index, newest_page_index)

    def test_sort_alphabetical(self):
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Apple',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Banana',
        )

        response = self.client.get(
            self.library_page.url,
            data={'sort': self.library_page.SORT_ALPHABETICAL.value}
        )

        research_detail_pages = list(response.context['research_detail_pages'])
        apple_page_index = research_detail_pages.index(apple_page)
        banana_page_index = research_detail_pages.index(banana_page)
        self.assertLess(apple_page_index, banana_page_index)

    def test_sort_alphabetical_reversed(self):
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Apple',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Banana',
        )

        response = self.client.get(
            self.library_page.url,
            data={'sort': self.library_page.SORT_ALPHABETICAL_REVERSED.value}
        )

        research_detail_pages = list(response.context['research_detail_pages'])
        apple_page_index = research_detail_pages.index(apple_page)
        banana_page_index = research_detail_pages.index(banana_page)
        self.assertLess(banana_page_index, apple_page_index)

    def test_get_research_detail_pages_sort_default(self):
        research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2)
        )
        research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1)
        )

        default_response = self.client.get(self.library_page.url)
        newest_first_response = self.client.get(
            self.library_page.url,
            data={'sort': self.library_page.SORT_NEWEST_FIRST.value}
        )

        default_sort_detail_pages = list(
            default_response.context['research_detail_pages']
        )
        newest_first_detail_pages = list(
            newest_first_response.context['research_detail_pages']
        )
        self.assertEqual(default_sort_detail_pages, newest_first_detail_pages)

    def test_research_author_profile_in_context(self):
        detail_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )

        response = self.client.get(self.library_page.url)

        self.assertIn(
            detail_page.research_authors.first().author_profile,
            response.context['author_options'],
        )

    def test_non_research_author_profile_not_in_context(self):
        profile = profiles_factory.ProfileFactory()

        response = self.client.get(self.library_page.url)

        self.assertNotIn(
            profile,
            response.context['author_options'],
        )

    def test_research_author_in_context_aliased_detail_page_fr(self):
        '''
        After the treesync, there are alias pages in the non-default locales. But,
        before the pages are translated (a manual action) the related models like author
        are still the ones from the default locale.
        '''
        detail_page_en = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_en = detail_page_en.research_authors.first().author_profile
        self.synchronize_tree()
        translation.activate(self.fr_locale.language_code)

        response = self.client.get(self.library_page.localized.url)

        self.assertIn(
            profile_en,
            response.context['author_options'],
        )

    def test_research_author_in_context_translated_detail_page_fr(self):
        '''
        When a profile for the active locale exists, pass that one to the context.

        Profiles are not necessarily people, so they might have translated names.
        '''
        detail_page_en = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_en = detail_page_en.research_authors.first().author_profile
        self.synchronize_tree()
        detail_page_fr = research_test_utils.translate_detail_page(detail_page_en, self.fr_locale)
        profile_fr = detail_page_fr.research_authors.first().author_profile
        translation.activate(self.fr_locale.language_code)

        response = self.client.get(self.library_page.localized.url)

        self.assertNotIn(
            profile_en,
            response.context['author_options'],
        )
        self.assertIn(
            profile_fr,
            response.context['author_options'],
        )

    def test_filter_author_profile(self):
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        author_profile = detail_page_1.research_authors.first().author_profile
        self.assertNotEqual(
            author_profile,
            detail_page_2.research_authors.first().author_profile,
        )

        response = self.client.get(
            self.library_page.url,
            data={'author': author_profile.id},
        )

        research_detail_pages = response.context['research_detail_pages']
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_filter_multiple_author_profiles(self):
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_a = detail_page_1.research_authors.first().author_profile
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_b = detail_page_2.research_authors.first().author_profile
        # Make author of first page also an author of the second page
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=detail_page_2,
            author_profile=profile_a,
        )

        response = self.client.get(
            self.library_page.url,
            data={'author': [profile_a.id, profile_b.id]},
        )

        # Only show the page where both profiles are authors
        research_detail_pages = response.context['research_detail_pages']
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)

    def test_filter_localized_author_profile(self):
        '''
        When filtering for a localized author profile, we also want to show pages
        associated with the default locale's profile. This is because after tree sync,
        pages are copied to the different locales, but related models are still the ones
        from the default locale.

        This test is setting up an aliased page and a translated page. The aliased page
        is not associated with the translated profile, but we still want to see it in
        the results.
        '''
        profile = profiles_factory.ProfileFactory()
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            research_authors__author_profile=profile,
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
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

        response = self.client.get(
            self.library_page.localized.url,
            data={'author': profile_fr.id},
        )

        research_detail_pages = response.context['research_detail_pages']
        self.assertIn(detail_page_1_fr, research_detail_pages)
        self.assertIn(detail_page_2_fr, research_detail_pages)
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_research_topics_in_context(self):
        topic_1 = research_factory.ResearchTopicFactory()
        topic_2 = research_factory.ResearchTopicFactory()

        response = self.client.get(self.library_page.url)

        topic_options = response.context['topic_options']
        self.assertEqual(len(topic_options), 2)
        self.assertIn(topic_1, topic_options)
        self.assertIn(topic_2, topic_options)

    def test_topic_in_context_matches_active_locale(self):
        topic_en = research_factory.ResearchTopicFactory()
        topic_fr = topic_en.copy_for_translation(self.fr_locale)
        topic_fr.save()

        response_en = self.client.get(self.library_page.localized.url)
        translation.activate(self.fr_locale.language_code)
        response_fr = self.client.get(self.library_page.localized.url)

        topic_options_en = response_en.context['topic_options']
        self.assertEqual(len(topic_options_en), 1)
        self.assertIn(topic_en, topic_options_en)
        self.assertNotIn(topic_fr, topic_options_en)
        topic_options_fr = response_fr.context['topic_options']
        self.assertEqual(len(topic_options_fr), 1)
        self.assertNotIn(topic_en, topic_options_fr)
        self.assertIn(topic_fr, topic_options_fr)

    def test_localized_topic_options(self):
        '''
        Use active locales version of topic if available.

        If no translation is available for a given topic, display the default locale
        topic.

        '''
        topic_1_en = research_factory.ResearchTopicFactory()
        topic_1_fr = topic_1_en.copy_for_translation(self.fr_locale)
        topic_1_fr.save()
        topic_2_en = research_factory.ResearchTopicFactory()
        translation.activate(self.fr_locale.language_code)

        response = self.client.get(self.library_page.localized.url)

        topic_options = response.context['topic_options']
        self.assertEqual(len(topic_options), 2)
        self.assertNotIn(topic_1_en, topic_options)
        self.assertIn(topic_1_fr, topic_options)
        self.assertIn(topic_2_en, topic_options)

    def test_filter_topic(self):
        topic_A = research_factory.ResearchTopicFactory()
        detail_page_A = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__research_topic=topic_A,
        )
        topic_B = research_factory.ResearchTopicFactory()
        detail_page_B = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__research_topic=topic_B,
        )

        response = self.client.get(self.library_page.url, data={'topic': topic_A.id})

        research_detail_pages = response.context['research_detail_pages']
        self.assertIn(detail_page_A, research_detail_pages)
        self.assertNotIn(detail_page_B, research_detail_pages)

    def test_filter_multiple_topics(self):
        topic_A = research_factory.ResearchTopicFactory()
        topic_B = research_factory.ResearchTopicFactory()
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__research_topic=topic_A,
        )
        research_factory.ResearchDetailPageResearchTopicRelationFactory(
            research_detail_page=detail_page_1,
            research_topic=topic_B
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__research_topic=topic_A,
        )

        response = self.client.get(
            self.library_page.url,
            data={'topic': [topic_A.id, topic_B.id]}
        )

        research_detail_pages = response.context['research_detail_pages']
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_filter_localized_topic(self):
        '''
        When filtering for a localized topic, we also want to show pages
        associated with the default locale's topic. This is because after tree sync,
        pages are copied to the different locales, but related models are still the ones
        from the default locale.

        This test is setting up an aliased page and a translated page. The aliased page
        is not associated with the translated topic, but we still want to see it in
        the results.
        '''
        topic = research_factory.ResearchTopicFactory()
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_topics__research_topic=topic,
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
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

        response = self.client.get(
            self.library_page.localized.url,
            data={'topic': topic_fr.id},
        )

        research_detail_pages = response.context['research_detail_pages']
        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1_fr, research_detail_pages)
        self.assertIn(detail_page_2_fr, research_detail_pages)
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_research_regions_in_context(self):
        region_1 = research_factory.ResearchRegionFactory()
        region_2 = research_factory.ResearchRegionFactory()

        response = self.client.get(self.library_page.url)

        region_options = response.context['region_options']
        self.assertEqual(len(region_options), 2)
        self.assertIn(region_1, region_options)
        self.assertIn(region_2, region_options)

    def test_region_in_context_matches_active_locale(self):
        region_en = research_factory.ResearchRegionFactory()
        region_fr = region_en.copy_for_translation(self.fr_locale)
        region_fr.save()

        response_en = self.client.get(self.library_page.localized.url)
        translation.activate(self.fr_locale.language_code)
        response_fr = self.client.get(self.library_page.localized.url)

        region_options_en = response_en.context['region_options']
        self.assertEqual(len(region_options_en), 1)
        self.assertIn(region_en, region_options_en)
        self.assertNotIn(region_fr, region_options_en)
        region_options_fr = response_fr.context['region_options']
        self.assertEqual(len(region_options_fr), 1)
        self.assertNotIn(region_en, region_options_fr)
        self.assertIn(region_fr, region_options_fr)

    def test_localized_region_options(self):
        '''
        Use active locales version of region if available.

        If no translation is available for a given region, display the default locale
        region.

        '''
        region_1_en = research_factory.ResearchRegionFactory()
        region_1_fr = region_1_en.copy_for_translation(self.fr_locale)
        region_1_fr.save()
        region_2_en = research_factory.ResearchRegionFactory()
        translation.activate(self.fr_locale.language_code)

        response = self.client.get(self.library_page.localized.url)

        region_options = response.context['region_options']
        self.assertEqual(len(region_options), 2)
        self.assertNotIn(region_1_en, region_options)
        self.assertIn(region_1_fr, region_options)
        self.assertIn(region_2_en, region_options)

    def test_filter_region(self):
        region_A = research_factory.ResearchRegionFactory()
        detail_page_A = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__research_region=region_A,
        )
        region_B = research_factory.ResearchRegionFactory()
        detail_page_B = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__research_region=region_B,
        )

        response = self.client.get(self.library_page.url, data={'region': region_A.id})

        research_detail_pages = response.context['research_detail_pages']
        self.assertIn(detail_page_A, research_detail_pages)
        self.assertNotIn(detail_page_B, research_detail_pages)

    def test_filter_multiple_regions(self):
        region_A = research_factory.ResearchRegionFactory()
        region_B = research_factory.ResearchRegionFactory()
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__research_region=region_A,
        )
        research_factory.ResearchDetailPageResearchRegionRelationFactory(
            research_detail_page=detail_page_1,
            research_region=region_B
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__research_region=region_A,
        )

        response = self.client.get(
            self.library_page.url,
            data={'region': [region_A.id, region_B.id]}
        )

        research_detail_pages = response.context['research_detail_pages']
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_filter_localized_region(self):
        '''
        When filtering for a localized region, we also want to show pages
        associated with the default locale's region. This is because after tree sync,
        pages are copied to the different locales, but related models are still the ones
        from the default locale.

        This test is setting up an aliased page and a translated page. The aliased page
        is not associated with the translated region, but we still want to see it in
        the results.
        '''
        region = research_factory.ResearchRegionFactory()
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            related_regions__research_region=region,
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
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
            data={'region': region_fr.id},
        )

        research_detail_pages = response.context['research_detail_pages']
        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1_fr, research_detail_pages)
        self.assertIn(detail_page_2_fr, research_detail_pages)
        self.assertNotIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_years_in_context(self):
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        year_1 = detail_page_1.original_publication_date.year
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        year_2 = detail_page_2.original_publication_date.year

        response = self.client.get(self.library_page.url)

        year_options = response.context['year_options']
        self.assertEqual(len(year_options), 2)
        self.assertIn(year_1, year_options)
        self.assertIn(year_2, year_options)

    def test_filter_for_year(self):
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        year_1 = detail_page_1.original_publication_date.year
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=datetime.date(year_1 + 1, 6, 1)
        )

        response = self.client.get(self.library_page.url, data={'year': year_1})

        research_detail_pages = response.context['research_detail_pages']
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertNotIn(detail_page_2, research_detail_pages)

    def test_library_page_breadcrumbs(self):
        response = self.client.get(self.library_page.url)
        breadcrumbs = response.context['breadcrumbs']
        expected_breadcrumbs = [{'title': 'Research', 'url': '/en/research/'}]

        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs, expected_breadcrumbs)

    def test_pagination(self):
        self.library_page.results_count = 4
        self.library_page.save()
        for _ in range(6):
            research_factory.ResearchDetailPageFactory(parent=self.library_page)

        first_page_response = self.client.get(self.library_page.url, data={'page': 1})
        second_page_response = self.client.get(self.library_page.url, data={'page': 2})

        first_page_detail_pages = first_page_response.context['research_detail_pages']
        self.assertEqual(len(first_page_detail_pages), 4)
        second_page_detail_pages = second_page_response.context['research_detail_pages']
        self.assertEqual(len(second_page_detail_pages), 2)
