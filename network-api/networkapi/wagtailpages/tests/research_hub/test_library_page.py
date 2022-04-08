import unittest

from networkapi.wagtailpages.factory import profiles as profiles_factory
from networkapi.wagtailpages.factory import research_hub as research_factory
from networkapi.wagtailpages.tests.research_hub import base as research_test_base
from networkapi.wagtailpages.tests.research_hub import utils as research_test_utils


class TestResearchLibraryPage(research_test_base.ResearchHubTestCase):
    def test_get_research_detail_pages(self):
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )

        research_detail_pages = self.library_page.get_research_detail_pages()

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)

    def test_get_research_detail_pages_with_translation_aliases(self):
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        self.synchronize_tree()
        fr_detail_page_1 = detail_page_1.get_translation(self.fr_locale)
        fr_detail_page_2 = detail_page_2.get_translation(self.fr_locale)

        research_detail_pages = self.library_page.get_research_detail_pages()

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)
        self.assertNotIn(fr_detail_page_1, research_detail_pages)
        self.assertNotIn(fr_detail_page_2, research_detail_pages)

    def test_get_research_detail_pages_search_by_title(self):
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

        research_detail_pages = self.library_page.get_research_detail_pages(
            search='Apple',
        )

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_get_research_detail_pages_search_by_introduction(self):
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

        research_detail_pages = self.library_page.get_research_detail_pages(
            search='Apple',
        )

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_get_research_detail_pages_search_by_overview(self):
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

        research_detail_pages = self.library_page.get_research_detail_pages(
            search='Apple',
        )

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_get_research_detail_pages_search_by_collaborators(self):
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

        research_detail_pages = self.library_page.get_research_detail_pages(
            search='Apple',
        )

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    @unittest.expectedFailure
    def test_get_research_detail_pages_search_by_author_name(self):
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

        research_detail_pages = self.library_page.get_research_detail_pages(
            search='Apple',
        )

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_get_research_detail_pages_sort_newest_first(self):
        oldest_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2)
        )
        newest_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1)
        )

        research_detail_pages = list(
            self.library_page.get_research_detail_pages(
                sort=self.library_page.SORT_NEWEST_FIRST
            )
        )

        newest_page_index = research_detail_pages.index(newest_page)
        oldest_page_index = research_detail_pages.index(oldest_page)
        self.assertLess(newest_page_index, oldest_page_index)

    def test_get_research_detail_pages_sort_oldest_first(self):
        oldest_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2)
        )
        newest_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1)
        )

        research_detail_pages = list(
            self.library_page.get_research_detail_pages(
                sort=self.library_page.SORT_OLDEST_FIRST
            )
        )

        newest_page_index = research_detail_pages.index(newest_page)
        oldest_page_index = research_detail_pages.index(oldest_page)
        self.assertLess(oldest_page_index, newest_page_index)

    def test_get_research_detail_pages_sort_alphabetical(self):
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Apple',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Banana',
        )

        research_detail_pages = list(
            self.library_page.get_research_detail_pages(
                sort=self.library_page.SORT_ALPHABETICAL
            )
        )

        apple_page_index = research_detail_pages.index(apple_page)
        banana_page_index = research_detail_pages.index(banana_page)
        self.assertLess(apple_page_index, banana_page_index)

    def test_get_research_detail_pages_sort_alphabetical_reversed(self):
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Apple',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Banana',
        )

        research_detail_pages = list(
            self.library_page.get_research_detail_pages(
                sort=self.library_page.SORT_ALPHABETICAL_REVERSED
            )
        )

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

        default_sort_result = list(self.library_page.get_research_detail_pages())
        newest_first_result = list(
            self.library_page.get_research_detail_pages(
                sort=self.library_page.SORT_NEWEST_FIRST
            )
        )

        self.assertEqual(default_sort_result, newest_first_result)
