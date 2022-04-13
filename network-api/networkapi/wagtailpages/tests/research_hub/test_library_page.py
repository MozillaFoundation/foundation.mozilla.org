import unittest

from django.utils import translation

from networkapi.wagtailpages.factory import profiles as profiles_factory
from networkapi.wagtailpages.factory import research_hub as research_factory
from networkapi.wagtailpages.tests.research_hub import base as research_test_base
from networkapi.wagtailpages.tests.research_hub import utils as research_test_utils


class TestResearchLibraryPage(research_test_base.ResearchHubTestCase):
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

    @unittest.expectedFailure
    def test_search_by_detail_page_author_name(self):
        '''
        Test detail page can be searched by author profile name.

        While it will also be possible to filter by author name, it would seem odd
        that the main author names can not be searched, while the collaborators can.

        Foreign key relations can be indexed for Wagtail search with
        `index.RelatedFields`. This does unfortunately not work for models related with
        a through model. For through model relations to be indexable, we would need
        to create a callable or attribute and index that. That functionality is only
        available with the ElasticSearch backend. Therefore, until we switch the search
        backend, this test is marked as an expected failure.

        See also:
        https://docs.wagtail.org/en/stable/topics/search/indexing.html#indexing-callables-and-other-attributes

        '''
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
        detail_page_fr = translate_detail_page(detail_page_en, self.fr_locale)
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

    # TODO: Filtering for localized value will show detail pages associated with localized value or origninal value, but preferes localized value. Just like the author detail page.
    #       This is necessary, because the detail page might be alias, but not translated. That means the detail page exists in the current locale but it is still associate with the author/region/topic of the default locale

# TODO: Move to helper module and use in test_author_index
def translate_detail_page(detail_page, locale):
    # Requires previous tree synchronization
    trans_detail_page = detail_page.get_translation(locale)

    for research_author_trans in trans_detail_page.research_authors.all():
        # The through model is already for the new locale after the tree sync,
        # but the related model is not.
        author_profile_orig = research_author_trans.author_profile
        author_profile_trans = author_profile_orig.copy_for_translation(locale)
        author_profile_trans.save()
        research_author_trans.author_profile = author_profile_trans
        research_author_trans.save()

    trans_detail_page.alias_of = None
    trans_detail_page.save()
    return trans_detail_page
