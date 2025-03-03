import os

from django.core import management, paginator
from django.utils import translation

from foundation_cms.legacy_cms.wagtailpages.factory import profiles as profiles_factory
from foundation_cms.legacy_cms.wagtailpages.factory.libraries.rcc import (
    detail_page as detail_page_factory,
)
from foundation_cms.legacy_cms.wagtailpages.factory.libraries.rcc import relations as relations_factory
from foundation_cms.legacy_cms.wagtailpages.factory.libraries.rcc import (
    taxonomies as taxonomies_factory,
)
from foundation_cms.legacy_cms.wagtailpages.pagemodels.libraries import constants
from foundation_cms.legacy_cms.wagtailpages.pagemodels.libraries.rcc.forms import (
    RCCLibraryPageFilterForm,
)
from foundation_cms.legacy_cms.wagtailpages.tests.libraries.rcc import base as rcc_test_base
from foundation_cms.legacy_cms.wagtailpages.tests.libraries.rcc import utils as rcc_test_utils


class TestRCCLibraryPage(rcc_test_base.RCCTestCase):
    def update_index(self):
        with open(os.devnull, "w") as f:
            management.call_command("update_index", verbosity=0, stdout=f)

    def test_get_sorted_filtered_detail_pages(self):
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages()

        self.assertEqual(len(rcc_detail_pages), 2)
        self.assertIn(detail_page_1, rcc_detail_pages)
        self.assertIn(detail_page_2, rcc_detail_pages)

    def test_get_sorted_filtered_detail_pages_with_translation_aliases(self):
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        self.synchronize_tree()
        fr_detail_page_1 = detail_page_1.get_translation(self.fr_locale)
        fr_detail_page_2 = detail_page_2.get_translation(self.fr_locale)

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages()

        self.assertEqual(len(rcc_detail_pages), 2)
        self.assertIn(detail_page_1, rcc_detail_pages)
        self.assertIn(detail_page_2, rcc_detail_pages)
        self.assertNotIn(fr_detail_page_1, rcc_detail_pages)
        self.assertNotIn(fr_detail_page_2, rcc_detail_pages)

    def test_private_detail_pages_are_hidden(self):
        public_detail_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        private_detail_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        self.make_page_private(private_detail_page)

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages()
        self.assertEqual(len(rcc_detail_pages), 1)
        self.assertIn(public_detail_page, rcc_detail_pages)
        self.assertNotIn(private_detail_page, rcc_detail_pages)

    def test_sort_newest_first(self):
        oldest_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=rcc_test_utils.days_ago(2),
        )
        newest_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=rcc_test_utils.days_ago(1),
        )

        rcc_detail_pages = list(self.library_page.get_sorted_filtered_detail_pages(sort=constants.SORT_NEWEST_FIRST))

        newest_page_index = rcc_detail_pages.index(newest_page)
        oldest_page_index = rcc_detail_pages.index(oldest_page)
        self.assertLess(newest_page_index, oldest_page_index)

    def test_sort_oldest_first(self):
        oldest_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=rcc_test_utils.days_ago(2),
        )
        newest_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=rcc_test_utils.days_ago(1),
        )

        rcc_detail_pages = list(self.library_page.get_sorted_filtered_detail_pages(sort=constants.SORT_OLDEST_FIRST))

        newest_page_index = rcc_detail_pages.index(newest_page)
        oldest_page_index = rcc_detail_pages.index(oldest_page)
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

        rcc_detail_pages = list(self.library_page.get_sorted_filtered_detail_pages(sort=constants.SORT_ALPHABETICAL))

        apple_page_index = rcc_detail_pages.index(apple_page)
        banana_page_index = rcc_detail_pages.index(banana_page)
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

        rcc_detail_pages = list(
            self.library_page.get_sorted_filtered_detail_pages(sort=constants.SORT_ALPHABETICAL_REVERSED)
        )

        apple_page_index = rcc_detail_pages.index(apple_page)
        banana_page_index = rcc_detail_pages.index(banana_page)
        self.assertLess(banana_page_index, apple_page_index)

    def testget_sorted_filtered_detail_pages_sort_default(self):
        detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=rcc_test_utils.days_ago(2),
        )
        detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            original_publication_date=rcc_test_utils.days_ago(1),
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
            detail_page_factory.RCCDetailPageFactory(parent=self.library_page)

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages()

        rcc_detail_pages_paginator = paginator.Paginator(
            object_list=rcc_detail_pages,
            per_page=self.library_page.results_count,
            allow_empty_first_page=True,
        )

        first_page_response = rcc_detail_pages_paginator.get_page(1)
        second_page_response = rcc_detail_pages_paginator.get_page(2)

        self.assertEqual(len(first_page_response), 4)
        self.assertEqual(len(second_page_response), 2)


class TestRCCLibraryPageSearch(TestRCCLibraryPage):
    def test_search_by_detail_page_title(self):
        # Fields other than title are empty to avoid accidental test failures due to
        # fake data generation.
        apple_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Apple",
            introduction="",
            overview="",
            collaborators="",
        )
        banana_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Banana",
            introduction="",
            overview="",
            collaborators="",
        )

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")
        self.assertEqual(len(rcc_detail_pages), 1)
        self.assertIn(apple_page, rcc_detail_pages)
        self.assertNotIn(banana_page, rcc_detail_pages)

    def test_search_by_detail_page_introduction(self):
        apple_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="Apple",
            overview="",
            collaborators="",
        )
        banana_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="Banana",
            overview="",
            collaborators="",
        )

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(rcc_detail_pages), 1)
        self.assertIn(apple_page, rcc_detail_pages)
        self.assertNotIn(banana_page, rcc_detail_pages)

    def test_search_by_detail_page_overview(self):
        apple_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="",
            overview="Apple",
            collaborators="",
        )
        banana_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="",
            overview="Banana",
            collaborators="",
        )

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(rcc_detail_pages), 1)
        self.assertIn(apple_page, rcc_detail_pages)
        self.assertNotIn(banana_page, rcc_detail_pages)

    def test_search_by_detail_page_collaborators(self):
        apple_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="",
            overview="",
            collaborators="Apple",
        )
        banana_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="",
            overview="",
            collaborators="Banana",
        )

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(rcc_detail_pages), 1)
        self.assertIn(apple_page, rcc_detail_pages)
        self.assertNotIn(banana_page, rcc_detail_pages)

    def test_search_by_detail_page_author_name(self):
        """Test detail page can be searched by author profile name."""
        apple_page = detail_page_factory.RCCDetailPageFactory(
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
        relations_factory.RCCAuthorRelationFactory(detail_page=apple_page, author_profile=apple_profile)
        banana_page = detail_page_factory.RCCDetailPageFactory(
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
        relations_factory.RCCAuthorRelationFactory(detail_page=banana_page, author_profile=banana_profile)
        self.update_index()

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(rcc_detail_pages), 1)
        self.assertIn(apple_page, rcc_detail_pages)
        self.assertNotIn(banana_page, rcc_detail_pages)

    def test_search_by_detail_page_content_type_name(self):
        """Test detail page can be searched by content type taxonomy name."""
        apple_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        apple_content_type = taxonomies_factory.RCCContentTypeFactory(
            name="Apple",
        )
        relations_factory.RCCDetailPageRCCContentTypeRelationFactory(
            detail_page=apple_page, content_type=apple_content_type
        )
        banana_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        banana_content_type = taxonomies_factory.RCCContentTypeFactory(
            name="banana",
        )
        relations_factory.RCCDetailPageRCCContentTypeRelationFactory(
            detail_page=banana_page, content_type=banana_content_type
        )
        self.update_index()

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(rcc_detail_pages), 1)
        self.assertIn(apple_page, rcc_detail_pages)
        self.assertNotIn(banana_page, rcc_detail_pages)

    def test_search_by_detail_page_curricular_area_name(self):
        """Test detail page can be searched by curricular_area taxonomy name."""
        apple_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        apple_curricular_area = taxonomies_factory.RCCCurricularAreaFactory(
            name="Apple",
        )
        relations_factory.RCCDetailPageRCCCurricularAreaRelationFactory(
            detail_page=apple_page, curricular_area=apple_curricular_area
        )
        banana_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        banana_curricular_area = taxonomies_factory.RCCCurricularAreaFactory(
            name="banana",
        )
        relations_factory.RCCDetailPageRCCCurricularAreaRelationFactory(
            detail_page=banana_page, curricular_area=banana_curricular_area
        )
        self.update_index()

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(rcc_detail_pages), 1)
        self.assertIn(apple_page, rcc_detail_pages)
        self.assertNotIn(banana_page, rcc_detail_pages)

    def test_search_by_detail_page_topic_name(self):
        """Test detail page can be searched by topic name."""
        apple_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        apple_topic = taxonomies_factory.RCCTopicFactory(
            name="Apple",
        )
        relations_factory.RCCDetailPageRCCTopicRelationFactory(detail_page=apple_page, topic=apple_topic)
        banana_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            title="Also cherry",
            introduction="",
            overview="",
            collaborators="",
        )
        banana_topic = taxonomies_factory.RCCTopicFactory(
            name="banana",
        )
        relations_factory.RCCDetailPageRCCTopicRelationFactory(detail_page=banana_page, topic=banana_topic)
        self.update_index()

        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(search_query="Apple")

        self.assertEqual(len(rcc_detail_pages), 1)
        self.assertIn(apple_page, rcc_detail_pages)
        self.assertNotIn(banana_page, rcc_detail_pages)


class TestRCCLibraryPageFilters(TestRCCLibraryPage):
    def test_filter_author_profile(self):
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        author_profile = detail_page_1.authors.first().author_profile
        self.assertNotEqual(
            author_profile,
            detail_page_2.authors.first().author_profile,
        )

        filter_form = RCCLibraryPageFilterForm(data={"authors": [author_profile.id]})
        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_1, rcc_detail_pages)
        self.assertNotIn(detail_page_2, rcc_detail_pages)

    def test_filter_multiple_author_profiles(self):
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        profile_a = detail_page_1.authors.first().author_profile
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        profile_b = detail_page_2.authors.first().author_profile
        # Make author of first page also an author of the second page
        relations_factory.RCCAuthorRelationFactory(
            detail_page=detail_page_2,
            author_profile=profile_a,
        )

        response = self.client.get(
            self.library_page.url,
            data={"authors": [profile_a.id, profile_b.id]},
        )

        # Only show the page where both profiles are authors
        rcc_detail_pages = response.context["detail_pages"]
        self.assertNotIn(detail_page_1, rcc_detail_pages)
        self.assertIn(detail_page_2, rcc_detail_pages)

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
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            authors__author_profile=profile,
        )
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            authors__author_profile=profile,
        )
        self.synchronize_tree()
        detail_page_1_fr = detail_page_1.get_translation(self.fr_locale)
        self.assertEqual(profile, detail_page_1_fr.authors.first().author_profile)
        detail_page_2_fr = rcc_test_utils.translate_detail_page(detail_page_2, self.fr_locale)
        profile_fr = detail_page_2_fr.authors.first().author_profile
        self.assertNotEqual(profile, profile_fr)
        self.assertEqual(profile.translation_key, profile_fr.translation_key)
        translation.activate(self.fr_locale.language_code)

        filter_form = RCCLibraryPageFilterForm(data={"authors": [profile_fr.id]})
        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_1_fr, rcc_detail_pages)
        self.assertIn(detail_page_2_fr, rcc_detail_pages)
        self.assertNotIn(detail_page_1, rcc_detail_pages)
        self.assertNotIn(detail_page_2, rcc_detail_pages)

    def test_filter_content_type(self):
        content_type_A = taxonomies_factory.RCCContentTypeFactory()
        detail_page_A = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_content_types__content_type=content_type_A,
        )
        content_type_B = taxonomies_factory.RCCContentTypeFactory()
        detail_page_B = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_content_types__content_type=content_type_B,
        )

        filter_form = RCCLibraryPageFilterForm(data={"content_types": [content_type_A.id]})
        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_A, rcc_detail_pages)
        self.assertNotIn(detail_page_B, rcc_detail_pages)

    def test_filter_curricular_area(self):
        curricular_area_A = taxonomies_factory.RCCCurricularAreaFactory()
        detail_page_A = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_curricular_areas__curricular_area=curricular_area_A,
        )
        curricular_area_B = taxonomies_factory.RCCCurricularAreaFactory()
        detail_page_B = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_curricular_areas__curricular_area=curricular_area_B,
        )

        filter_form = RCCLibraryPageFilterForm(data={"curricular_areas": [curricular_area_A.id]})
        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_A, rcc_detail_pages)
        self.assertNotIn(detail_page_B, rcc_detail_pages)

    def test_filter_topic(self):
        topic_A = taxonomies_factory.RCCTopicFactory()
        detail_page_A = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic_A,
        )
        topic_B = taxonomies_factory.RCCTopicFactory()
        detail_page_B = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic_B,
        )

        filter_form = RCCLibraryPageFilterForm(data={"topics": [topic_A.id]})
        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_A, rcc_detail_pages)
        self.assertNotIn(detail_page_B, rcc_detail_pages)

    def test_filter_multiple_content_types(self):
        content_type_A = taxonomies_factory.RCCContentTypeFactory()
        content_type_B = taxonomies_factory.RCCContentTypeFactory()
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_content_types__content_type=content_type_A,
        )
        relations_factory.RCCDetailPageRCCContentTypeRelationFactory(
            detail_page=detail_page_1, content_type=content_type_B
        )
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_content_types__content_type=content_type_A,
        )

        filter_form = RCCLibraryPageFilterForm(data={"content_types": [content_type_A.id, content_type_B.id]})
        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_1, rcc_detail_pages)
        self.assertNotIn(detail_page_2, rcc_detail_pages)

    def test_filter_multiple_curricular_areas(self):
        curricular_area_A = taxonomies_factory.RCCCurricularAreaFactory()
        curricular_area_B = taxonomies_factory.RCCCurricularAreaFactory()
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_curricular_areas__curricular_area=curricular_area_A,
        )
        relations_factory.RCCDetailPageRCCCurricularAreaRelationFactory(
            detail_page=detail_page_1, curricular_area=curricular_area_B
        )
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_curricular_areas__curricular_area=curricular_area_A,
        )

        filter_form = RCCLibraryPageFilterForm(data={"curricular_areas": [curricular_area_A.id, curricular_area_B.id]})
        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_1, rcc_detail_pages)
        self.assertNotIn(detail_page_2, rcc_detail_pages)

    def test_filter_multiple_topics(self):
        topic_A = taxonomies_factory.RCCTopicFactory()
        topic_B = taxonomies_factory.RCCTopicFactory()
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic_A,
        )
        relations_factory.RCCDetailPageRCCTopicRelationFactory(detail_page=detail_page_1, topic=topic_B)
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic_A,
        )

        filter_form = RCCLibraryPageFilterForm(data={"topics": [topic_A.id, topic_B.id]})
        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertIn(detail_page_1, rcc_detail_pages)
        self.assertNotIn(detail_page_2, rcc_detail_pages)

    def test_filter_localized_content_type(self):
        """
        When filtering for a localized content type, we also want to show pages
        associated with the default locale's content type. This is because after tree sync,
        pages are copied to the different locales, but related models are still the ones
        from the default locale.

        This test is setting up an aliased page and a translated page. The aliased page
        is not associated with the translated content type, but we still want to see it in
        the results.
        """
        content_type = taxonomies_factory.RCCContentTypeFactory()
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_content_types__content_type=content_type,
        )
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_content_types__content_type=content_type,
        )
        self.synchronize_tree()

        # Translate the first page, but not the content type
        detail_page_1_fr = detail_page_1.get_translation(self.fr_locale)
        # The translated page should have the same content type as the default page
        self.assertEqual(content_type, detail_page_1_fr.related_content_types.first().content_type)

        # Translate the second page and the content type
        detail_page_2_fr = rcc_test_utils.translate_detail_page(detail_page_2, self.fr_locale)
        content_type_fr = detail_page_2_fr.related_content_types.first().content_type
        self.assertNotEqual(content_type, content_type_fr)
        self.assertEqual(content_type.translation_key, content_type_fr.translation_key)

        # Switch to the French locale
        translation.activate(self.fr_locale.language_code)

        # Filter for the translated content type
        filter_form = RCCLibraryPageFilterForm(data={"content_types": [content_type_fr.id]})
        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        # We should see both pages, even though the first one is not associated with the
        # translated content type
        self.assertEqual(len(rcc_detail_pages), 2)
        self.assertIn(detail_page_1_fr, rcc_detail_pages)
        self.assertIn(detail_page_2_fr, rcc_detail_pages)
        self.assertNotIn(detail_page_1, rcc_detail_pages)
        self.assertNotIn(detail_page_2, rcc_detail_pages)

    def test_filter_localized_curricular_area(self):
        """
        When filtering for a localized curricular area, we also want to show pages
        associated with the default locale's curricular area. This is because after tree sync,
        pages are copied to the different locales, but related models are still the ones
        from the default locale.

        This test is setting up an aliased page and a translated page. The aliased page
        is not associated with the translated curricular area, but we still want to see it in
        the results.
        """
        curricular_area = taxonomies_factory.RCCCurricularAreaFactory()
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_curricular_areas__curricular_area=curricular_area,
        )
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_curricular_areas__curricular_area=curricular_area,
        )
        self.synchronize_tree()

        # Translate the first page, but not the curricular area
        detail_page_1_fr = detail_page_1.get_translation(self.fr_locale)
        # The translated page should have the same curricular area as the default page
        self.assertEqual(curricular_area, detail_page_1_fr.related_curricular_areas.first().curricular_area)

        # Translate the second page and the curricular area
        detail_page_2_fr = rcc_test_utils.translate_detail_page(detail_page_2, self.fr_locale)
        curricular_area_fr = detail_page_2_fr.related_curricular_areas.first().curricular_area
        self.assertNotEqual(curricular_area, curricular_area_fr)
        self.assertEqual(curricular_area.translation_key, curricular_area_fr.translation_key)

        # Switch to the French locale
        translation.activate(self.fr_locale.language_code)

        # Filter for the translated curricular area
        filter_form = RCCLibraryPageFilterForm(data={"curricular_area": [curricular_area_fr.id]})
        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        # We should see both pages, even though the first one is not associated with the
        # translated curricular area
        self.assertEqual(len(rcc_detail_pages), 2)
        self.assertIn(detail_page_1_fr, rcc_detail_pages)
        self.assertIn(detail_page_2_fr, rcc_detail_pages)
        self.assertNotIn(detail_page_1, rcc_detail_pages)
        self.assertNotIn(detail_page_2, rcc_detail_pages)

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
        topic = taxonomies_factory.RCCTopicFactory()
        detail_page_1 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic,
        )
        detail_page_2 = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            related_topics__topic=topic,
        )
        self.synchronize_tree()
        detail_page_1_fr = detail_page_1.get_translation(self.fr_locale)
        self.assertEqual(topic, detail_page_1_fr.related_topics.first().topic)
        detail_page_2_fr = rcc_test_utils.translate_detail_page(detail_page_2, self.fr_locale)
        topic_fr = detail_page_2_fr.related_topics.first().topic
        self.assertNotEqual(topic, topic_fr)
        self.assertEqual(topic.translation_key, topic_fr.translation_key)
        translation.activate(self.fr_locale.language_code)

        filter_form = RCCLibraryPageFilterForm(data={"topics": [topic_fr.id]})
        rcc_detail_pages = self.library_page.get_sorted_filtered_detail_pages(filter_form=filter_form)

        self.assertEqual(len(rcc_detail_pages), 2)
        self.assertIn(detail_page_1_fr, rcc_detail_pages)
        self.assertIn(detail_page_2_fr, rcc_detail_pages)
        self.assertNotIn(detail_page_1, rcc_detail_pages)
        self.assertNotIn(detail_page_2, rcc_detail_pages)
