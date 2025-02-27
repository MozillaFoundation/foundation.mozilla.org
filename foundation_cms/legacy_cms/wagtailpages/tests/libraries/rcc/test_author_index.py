import http

from django.utils import translation
from wagtail_localize import synctree

from legacy_cms.wagtailpages.factory import profiles as profiles_factory
from legacy_cms.wagtailpages.factory.libraries.rcc import relations as relations_factory
from legacy_cms.wagtailpages.tests.libraries.rcc import base as rcc_test_base
from legacy_cms.wagtailpages.tests.libraries.rcc import utils as rcc_test_utils


class TestRCCAuthorIndexPage(rcc_test_base.RCCTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.detail_page = cls.create_rcc_detail_page_on_parent(parent=cls.library_page, days_ago=14)
        cls.rcc_profile = profiles_factory.ProfileFactory()
        cls.rcc_profile.refresh_from_db()
        relations_factory.RCCAuthorRelationFactory(
            detail_page=cls.detail_page,
            author_profile=cls.rcc_profile,
        )

        cls.non_rcc_profile = profiles_factory.ProfileFactory()
        cls.non_rcc_profile.refresh_from_db()

    def setUp(self):
        super().setUp()
        translation.activate(self.default_locale.language_code)
        self.fr_detail_page = self.detail_page.get_translation(self.fr_locale)

    def translate_rcc_profile(self):
        self.fr_profile = self.rcc_profile.copy_for_translation(self.fr_locale)
        self.fr_profile.save()
        self.fr_profile.refresh_from_db()

    def create_rcc_detail_page_with_author(self, author_profile, days_ago=0):
        detail_page = self.create_rcc_detail_page(days_ago=days_ago)
        relations_factory.RCCAuthorRelationFactory(
            detail_page=detail_page,
            author_profile=author_profile,
        )
        return detail_page

    def test_author_profiles_prop(self):
        author_profiles = self.author_index.author_profiles
        self.translate_rcc_profile()

        self.assertIn(self.rcc_profile, author_profiles)
        # Non-rcc profile should not show up
        self.assertNotIn(self.non_rcc_profile, author_profiles)
        # Translated profile should not show up
        self.assertNotIn(self.fr_profile, author_profiles)

    def test_author_profiles_fr_locale_detail_alias(self):
        translation.activate(self.fr_locale.language_code)

        fr_author_profiles = self.author_index.localized.author_profiles

        # When the profile is not translated, the default locales profile should show
        self.assertIn(self.rcc_profile, fr_author_profiles)

    def test_author_profiles_fr_locale_detail_translated(self):
        fr_detail_page = rcc_test_utils.translate_detail_page(
            self.detail_page,
            self.fr_locale,
        )
        fr_profile = fr_detail_page.authors.first().author_profile
        translation.activate(self.fr_locale.language_code)

        # Get author_profiles when fr is active
        fr_author_profiles = self.author_index.localized.author_profiles

        self.assertNotIn(self.rcc_profile, fr_author_profiles)
        self.assertIn(fr_profile, fr_author_profiles)

    def test_profile_route(self):
        url = f"{ self.author_index.url }{ self.rcc_profile.slug }"

        response = self.client.get(url, follow=True)

        self.assertContains(
            response,
            text=self.rcc_profile.name,
            status_code=http.HTTPStatus.OK,
        )

    def test_profile_route_with_non_rcc_profile(self):
        url = f"{ self.author_index.url }{ self.non_rcc_profile.slug }"

        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

    def test_get_author_detail_context(self):
        context = self.author_index.localized.get_author_detail_context(
            profile_slug=self.rcc_profile.slug,
        )

        self.assertIn(self.detail_page, context["latest_articles"])
        self.assertNotIn(self.fr_detail_page, context["latest_articles"])

    def test_get_author_detail_context_fr_locale(self):
        translation.activate(self.fr_locale.language_code)
        # When page trees are automatically synced, but have not really been translated,
        # the profile is not translated. So even when the fr locale is active it will
        # use the original profile
        localized_rcc_profile = self.rcc_profile.localized
        self.assertEqual(localized_rcc_profile, self.rcc_profile)

        context = self.author_index.localized.get_author_detail_context(
            profile_slug=localized_rcc_profile.slug,
        )

        # The displayed detail pages should be the aliased pages not the original ones.
        self.assertNotIn(self.detail_page, context["latest_articles"])
        self.assertIn(self.fr_detail_page, context["latest_articles"])

    def test_get_author_detail_context_alias_and_translation(self):
        # There can be mixed situations, where only some rcc associated with
        # a profile is properly translated, but others are still only aliased.
        fr_detail_page = rcc_test_utils.translate_detail_page(
            self.detail_page,
            self.fr_locale,
        )
        extra_detail_page = self.create_rcc_detail_page_with_author(author_profile=self.rcc_profile)
        self.synchronize_tree()
        # Grab the alias page. Note: This page is not really translated, so it is still
        # associated with the original profile.
        fr_extra_detail_page = extra_detail_page.get_translation(self.fr_locale)
        # Check localized profile
        localized_rcc_profile = self.rcc_profile.localized
        self.assertEqual(localized_rcc_profile, self.rcc_profile)

        context = self.author_index.localized.get_author_detail_context(
            profile_slug=localized_rcc_profile.slug,
        )

        # We need to make sure that the displayed works are picked based on the active
        # locale, rather than the locale of the profile we are looking at
        self.assertIn(self.detail_page, context["latest_articles"])
        self.assertIn(extra_detail_page, context["latest_articles"])
        self.assertNotIn(fr_detail_page, context["latest_articles"])
        self.assertNotIn(fr_extra_detail_page, context["latest_articles"])

    def test_get_author_detail_context_fr_locale_alias_and_translation(self):
        # There can be mixed situations, where only some rcc associated with
        # a profile is properly translated, but others are still only aliased.
        fr_detail_page = rcc_test_utils.translate_detail_page(
            self.detail_page,
            self.fr_locale,
        )
        extra_detail_page = self.create_rcc_detail_page_with_author(author_profile=self.rcc_profile)
        synctree.synchronize_tree(source_locale=self.default_locale, target_locale=self.fr_locale)
        # Grab the alias page. Note: This page is not really translated, so it is still
        # associated with the original profile.
        fr_extra_detail_page = extra_detail_page.get_translation(self.fr_locale)
        # Activate locale
        translation.activate(self.fr_locale.language_code)
        localized_rcc_profile = self.rcc_profile.localized
        self.assertNotEqual(localized_rcc_profile, self.rcc_profile)

        context = self.author_index.localized.get_author_detail_context(
            profile_slug=localized_rcc_profile.slug,
        )

        # We need to make sure that the displayed works are picked based on the active
        # locale, rather than the locale of the profile we are looking at
        self.assertNotIn(self.detail_page, context["latest_articles"])
        self.assertNotIn(extra_detail_page, context["latest_articles"])
        self.assertIn(fr_detail_page, context["latest_articles"])
        self.assertIn(fr_extra_detail_page, context["latest_articles"])

    def test_get_latest_articles_contains_latest_three_detail_pages(self):
        detail_page_1 = self.detail_page
        detail_page_2 = self.create_rcc_detail_page_with_author(author_profile=self.rcc_profile, days_ago=3)
        detail_page_3 = self.create_rcc_detail_page_with_author(author_profile=self.rcc_profile, days_ago=2)
        detail_page_4 = self.create_rcc_detail_page_with_author(author_profile=self.rcc_profile, days_ago=1)

        latest_articles = self.author_index.get_latest_author_articles(
            author_profile=self.rcc_profile,
        )

        self.assertEqual(len(latest_articles), 3)
        self.assertIn(detail_page_4, latest_articles)
        self.assertIn(detail_page_3, latest_articles)
        self.assertIn(detail_page_2, latest_articles)
        self.assertNotIn(detail_page_1, latest_articles)

    def test_get_author_rcc_count_return_number_of_associated_detail_pages(self):
        # One page already exists, creating one more
        self.create_rcc_detail_page_with_author(author_profile=self.rcc_profile)

        count = self.author_index.get_author_articles_count(author_profile=self.rcc_profile)

        self.assertEqual(count, 2)

    def test_get_author_rcc_returns_profile_related_detail_pages(self):
        detail_page_1 = self.detail_page
        detail_page_2 = self.create_rcc_detail_page_with_author(author_profile=self.rcc_profile, days_ago=3)
        detail_page_3 = self.create_rcc_detail_page_with_author(author_profile=self.rcc_profile, days_ago=2)
        detail_page_4 = self.create_rcc_detail_page_with_author(author_profile=self.rcc_profile, days_ago=1)

        # 3 queries = 1 for the detail pages, 1 for the locale, 1 for the page  view restrictions
        with self.assertNumQueries(3):
            author_rcc = self.author_index.get_author_articles(
                author_profile=self.rcc_profile,
            )

            self.assertIn(detail_page_1, author_rcc)
            self.assertIn(detail_page_2, author_rcc)
            self.assertIn(detail_page_3, author_rcc)
            self.assertIn(detail_page_4, author_rcc)

    def test_get_author_rcc_not_returns_unpublished_pages(self):
        detail_page_published = self.detail_page
        detail_page_unpublished = self.create_rcc_detail_page_with_author(
            author_profile=self.rcc_profile,
            days_ago=1,
        )
        detail_page_unpublished.unpublish()
        detail_page_unpublished.save()

        latest_articles = self.author_index.get_author_articles(
            author_profile=self.rcc_profile,
        )

        self.assertEqual(len(latest_articles), 1)
        self.assertIn(detail_page_published, latest_articles)
        self.assertNotIn(detail_page_unpublished, latest_articles)

    def test_get_author_rcc_not_returns_private_pages(self):
        detail_page_public = self.detail_page
        detail_page_private = self.create_rcc_detail_page_with_author(
            author_profile=self.rcc_profile,
            days_ago=1,
        )
        self.make_page_private(detail_page_private)

        latest_articles = self.author_index.get_author_articles(
            author_profile=self.rcc_profile,
        )

        self.assertEqual(len(latest_articles), 1)
        self.assertIn(detail_page_public, latest_articles)
        self.assertNotIn(detail_page_private, latest_articles)
