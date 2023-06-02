# import datetime
import os

from django.core import management, paginator

# from networkapi.wagtailpages.factory import profiles as profiles_factory
from networkapi.wagtailpages.factory.libraries.rcc import (
    detail_page as detail_page_factory,
)

# from networkapi.wagtailpages.factory.libraries.rcc import (
#     relations as relations_factory,
# )
# from networkapi.wagtailpages.factory.libraries.rcc import (
#     taxonomies as taxonomies_factory,
# )
from networkapi.wagtailpages.pagemodels.libraries.rcc import constants
from networkapi.wagtailpages.tests.libraries.rcc import base as research_test_base
from networkapi.wagtailpages.tests.libraries.rcc import utils as research_test_utils

# from django.utils import translation


class TestRCCLibraryPage(research_test_base.RCCTestCase):
    def update_index(self):
        with open(os.devnull, "w") as f:
            management.call_command("update_index", verbosity=0, stdout=f)

    def test_get_rcc_detail_pages(self):
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )

        research_detail_pages = self.library_page._get_rcc_detail_pages()

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)

    def test_get_rcc_detail_pages_with_translation_aliases(self):
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        self.synchronize_tree()
        fr_detail_page_1 = detail_page_1.get_translation(self.fr_locale)
        fr_detail_page_2 = detail_page_2.get_translation(self.fr_locale)

        research_detail_pages = self.library_page._get_rcc_detail_pages()

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)
        self.assertNotIn(fr_detail_page_1, research_detail_pages)
        self.assertNotIn(fr_detail_page_2, research_detail_pages)

    def test_private_detail_pages_are_hidden(self):
        public_detail_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        private_detail_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        self.make_page_private(private_detail_page)

        research_detail_pages = self.library_page._get_rcc_detail_pages()
        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(public_detail_page, research_detail_pages)
        self.assertNotIn(private_detail_page, research_detail_pages)

    def test_sort_newest_first(self):
        oldest_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2),
        )
        newest_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1),
        )

        research_detail_pages = list(self.library_page._get_rcc_detail_pages(sort=constants.SORT_NEWEST_FIRST))

        newest_page_index = research_detail_pages.index(newest_page)
        oldest_page_index = research_detail_pages.index(oldest_page)
        self.assertLess(newest_page_index, oldest_page_index)

    def test_sort_oldest_first(self):
        oldest_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2),
        )
        newest_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1),
        )

        research_detail_pages = list(self.library_page._get_rcc_detail_pages(sort=constants.SORT_OLDEST_FIRST))

        newest_page_index = research_detail_pages.index(newest_page)
        oldest_page_index = research_detail_pages.index(oldest_page)
        self.assertLess(oldest_page_index, newest_page_index)

    def test_sort_alphabetical(self):
        apple_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Apple",
        )
        banana_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Banana",
        )

        research_detail_pages = list(self.library_page._get_rcc_detail_pages(sort=constants.SORT_ALPHABETICAL))

        apple_page_index = research_detail_pages.index(apple_page)
        banana_page_index = research_detail_pages.index(banana_page)
        self.assertLess(apple_page_index, banana_page_index)

    def test_sort_alphabetical_reversed(self):

        apple_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Apple",
        )
        banana_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Banana",
        )

        research_detail_pages = list(
            self.library_page._get_rcc_detail_pages(sort=constants.SORT_ALPHABETICAL_REVERSED)
        )

        apple_page_index = research_detail_pages.index(apple_page)
        banana_page_index = research_detail_pages.index(banana_page)
        self.assertLess(banana_page_index, apple_page_index)

    def test_get_rcc_detail_pages_sort_default(self):

        detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(2),
        )
        detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=research_test_utils.days_ago(1),
        )

        default_sort_detail_pages = list(self.library_page._get_rcc_detail_pages())
        newest_first_detail_pages = list(self.library_page._get_rcc_detail_pages(sort=constants.SORT_NEWEST_FIRST))

        self.assertEqual(default_sort_detail_pages, newest_first_detail_pages)

    def test_pagination(self):
        self.library_page.results_count = 4
        self.library_page.save()
        for _ in range(6):
            detail_page_factory.RCCDetailPageFactory(parent=self.library_page)

        research_detail_pages = self.library_page._get_rcc_detail_pages()

        research_detail_pages_paginator = paginator.Paginator(
            object_list=research_detail_pages,
            per_page=self.library_page.results_count,
            allow_empty_first_page=True,
        )

        first_page_response = research_detail_pages_paginator.get_page(1)
        second_page_response = research_detail_pages_paginator.get_page(2)

        self.assertEqual(len(first_page_response), 4)
        self.assertEqual(len(second_page_response), 2)
