import wagtail_factories
from django.core import exceptions
from django.utils import translation

from networkapi.wagtailpages.factory.libraries.rcc import (
    detail_page as detail_page_factory,
)
from networkapi.wagtailpages.factory.libraries.rcc import relations as relations_factory
from networkapi.wagtailpages.models import ArticlePage, PublicationPage, RCCDetailPage
from networkapi.wagtailpages.pagemodels.libraries.rcc import authors_index
from networkapi.wagtailpages.tests.libraries.rcc import base as rcc_test_base
from networkapi.wagtailpages.tests.libraries.rcc import utils as rcc_test_utils


class TestRCCLibraryDetailPage(rcc_test_base.RCCTestCase):
    def test_children(self):
        self.assertAllowedSubpageTypes(
            parent_model=RCCDetailPage,
            child_models={ArticlePage, PublicationPage},
        )

    def test_localized_authors(self) -> None:
        """
        This method should return the profiles of all the page related rcc authors.
        """
        page_a_author_profiles = []
        page_a = detail_page_factory.RCCDetailPageFactory(parent=self.library_page, authors=[])
        page_b = detail_page_factory.RCCDetailPageFactory(parent=self.library_page)
        page_b_author_profile = page_b.authors.first().author_profile

        for _ in range(3):
            rcc_author_relation = relations_factory.RCCAuthorRelationFactory(detail_page=page_a)
            page_a_author_profiles.append(rcc_author_relation.author_profile)

        page_a_rcc_authors = page_a.localized_authors

        self.assertEqual(len(page_a_rcc_authors), 3)
        self.assertNotIn(page_b_author_profile, page_a_rcc_authors)
        self.assertIn(page_a_author_profiles[0], page_a_rcc_authors)
        self.assertIn(page_a_author_profiles[1], page_a_rcc_authors)
        self.assertIn(page_a_author_profiles[2], page_a_rcc_authors)

    def test_localized_authors_returns_localized_profiles(self) -> None:
        """
        If a related author's profile has a translated version available,
        this method should return it in the active locale.
        """
        detail_page = detail_page_factory.RCCDetailPageFactory(parent=self.library_page)
        profile_en = detail_page.authors.first().author_profile
        self.synchronize_tree()
        # Translating both the page and the rcc author profile
        detail_page_fr = rcc_test_utils.translate_detail_page(detail_page, self.fr_locale)
        profile_fr = detail_page_fr.authors.first().author_profile

        translation.activate(self.fr_locale.language_code)
        rcc_authors_fr = detail_page.localized.localized_authors

        self.assertEqual(len(rcc_authors_fr), 1)
        self.assertIn(profile_fr, rcc_authors_fr)
        self.assertNotIn(profile_en, rcc_authors_fr)

    def test_localized_authors_returns_localized_profiles_rendered(self) -> None:
        """
        Similar to the above, but these links get passed to routablepageurl in the template
        so we can be certain that they come out localized.
        """
        detail_page = detail_page_factory.RCCDetailPageFactory(parent=self.library_page)
        self.synchronize_tree()
        # Translating both the page and the rcc author profile.
        detail_page_fr = rcc_test_utils.translate_detail_page(detail_page, self.fr_locale)
        profile_fr = detail_page_fr.authors.first().author_profile
        translation.activate(self.fr_locale.language_code)
        author_index = authors_index.RCCAuthorsIndexPage.objects.first()
        fr_author_index = authors_index.RCCAuthorsIndexPage.objects.filter(locale=self.fr_locale).first()

        # Build a URL to check for in the response.
        # E.G, /fr/rcc/authors/1/name-here/
        fr_author_link = fr_author_index.url + fr_author_index.reverse_subpage(
            "rcc-author-detail", kwargs={"profile_slug": profile_fr.slug}
        )
        en_author_link = author_index.url + author_index.reverse_subpage(
            "rcc-author-detail", kwargs={"profile_slug": profile_fr.slug}
        )

        # Request the fr version of the page.
        response = self.client.get(detail_page_fr.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, fr_author_link)
        self.assertNotContains(response, en_author_link)

    def test_localized_authors_returns_default_locale(self) -> None:
        """
        If a related rcc author's profile does not have a translated version available,
        localized pages should return it in the default locale (English).
        """
        detail_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        profile_en = detail_page.authors.first().author_profile
        self.synchronize_tree()

        translation.activate(self.fr_locale.language_code)
        rcc_authors_fr = detail_page.localized.localized_authors

        self.assertEqual(len(rcc_authors_fr), 1)
        self.assertIn(profile_en, rcc_authors_fr)


class TestRCCDetailLink(rcc_test_base.RCCTestCase):
    def test_clean_with_url(self) -> None:
        link = detail_page_factory.RCCDetailLinkFactory.build(with_url=True)

        link.clean()

        self.assertTrue(link.url)
        self.assertFalse(link.page)
        self.assertFalse(link.document)

    def test_clean_with_page(self) -> None:
        link = detail_page_factory.RCCDetailLinkFactory.build(with_page=True)

        link.clean()

        self.assertTrue(link.page)
        self.assertFalse(link.url)
        self.assertFalse(link.document)

    def test_clean_with_doc(self) -> None:
        link = detail_page_factory.RCCDetailLinkFactory.build(with_document=True)

        link.clean()

        self.assertTrue(link.document)
        self.assertFalse(link.url)
        self.assertFalse(link.page)

    def test_clean_with_url_and_page(self) -> None:
        link = detail_page_factory.RCCDetailLinkFactory.build(
            with_url=True,
            with_page=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_url_and_doc(self) -> None:
        link = detail_page_factory.RCCDetailLinkFactory.build(
            with_url=True,
            with_document=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_page_and_doc(self) -> None:
        link = detail_page_factory.RCCDetailLinkFactory.build(
            with_url=True,
            with_page=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_url_and_page_and_doc(self) -> None:
        link = detail_page_factory.RCCDetailLinkFactory.build(
            with_url=True,
            with_page=True,
            with_document=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_neither_url_page_nor_doc(self):
        link = detail_page_factory.RCCDetailLinkFactory.build()

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_get_url_with_url(self) -> None:
        url = "https://example.com"
        link = detail_page_factory.RCCDetailLinkFactory.build(url=url)

        self.assertEqual(link.get_url(), url)

    def test_get_url_with_page(self) -> None:
        page = wagtail_factories.PageFactory(parent=self.homepage)
        link = detail_page_factory.RCCDetailLinkFactory.build(page=page)

        self.assertEqual(link.get_url(), page.get_url())

    def test_get_url_with_non_live_page(self) -> None:
        page = wagtail_factories.PageFactory(parent=self.homepage, live=False)
        link = detail_page_factory.RCCDetailLinkFactory.build(page=page)

        self.assertEqual(link.get_url(), "")

    def test_get_url_with_doc(self) -> None:
        doc = wagtail_factories.DocumentFactory()
        link = detail_page_factory.RCCDetailLinkFactory.build(document=doc)

        self.assertEqual(link.get_url(), doc.url)

    def test_get_url_without_needed_data(self) -> None:
        """
        Test the invalid link case.

        This link should raise a validation error when it is being created, but the `get_url` method still needs to
        handle this logic branch in a sensible manner.

        """
        link = detail_page_factory.RCCDetailLinkFactory.build()

        with self.assertRaises(ValueError):
            link.get_url()
