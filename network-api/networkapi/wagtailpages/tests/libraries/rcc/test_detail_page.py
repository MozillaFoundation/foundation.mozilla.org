# import wagtail_factories
# from django.core import exceptions
# from django.utils import translation

# from networkapi.wagtailpages.factory.libraries.rcc import (
#     detail_page as detail_page_factory,
# )
# from networkapi.wagtailpages.factory.libraries.rcc import (
#     relations as relations_factory,
# )
from networkapi.wagtailpages.models import ArticlePage, PublicationPage, RCCDetailPage

# from networkapi.wagtailpages.pagemodels.libraries.rcc import authors_index
from networkapi.wagtailpages.tests.libraries.rcc import base as rcc_test_base

# from networkapi.wagtailpages.tests.libraries.rcc import (
#     utils as rcc_test_utils,
# )


class TestRCCLibraryDetailPage(rcc_test_base.RCCHubTestCase):
    def test_children(self):
        self.assertAllowedSubpageTypes(
            parent_model=RCCDetailPage,
            child_models={ArticlePage, PublicationPage},
        )

    # def test_get_rcc_authors(self) -> None:
    #     """
    #     This method should return the profiles of all the page related rcc authors.
    #     """
    #     page_a_author_profiles = []
    #     page_a = detail_page_factory.RCCDetailPageFactory(parent=self.library_page, rcc_authors=[])
    #     page_b = detail_page_factory.RCCDetailPageFactory(parent=self.library_page)
    #     page_b_author_profile = page_b.rcc_authors.first().author_profile

    #     for _ in range(3):
    #         rcc_author_relation = relations_factory.RCCAuthorRelationFactory(rcc_detail_page=page_a)
    #         page_a_author_profiles.append(rcc_author_relation.author_profile)

    #     page_a_rcc_authors = page_a.get_rcc_authors()

    #     self.assertEqual(len(page_a_rcc_authors), 3)
    #     self.assertNotIn(page_b_author_profile, page_a_rcc_authors)
    #     self.assertIn(page_a_author_profiles[0], page_a_rcc_authors)
    #     self.assertIn(page_a_author_profiles[1], page_a_rcc_authors)
    #     self.assertIn(page_a_author_profiles[2], page_a_rcc_authors)

    # def test_get_rcc_authors_returns_localized_profiles(self) -> None:
    #     """
    #     If a related author's profile has a translated version available,
    #     this method should return it in the active locale.
    #     """
    #     detail_page = detail_page_factory.RCCDetailPageFactory(parent=self.library_page)
    #     profile_en = detail_page.rcc_authors.first().author_profile
    #     self.synchronize_tree()
    #     # Translating both the page and the rcc author profile
    #     detail_page_fr = rcc_test_utils.translate_detail_page(detail_page, self.fr_locale)
    #     profile_fr = detail_page_fr.rcc_authors.first().author_profile

    #     translation.activate(self.fr_locale.language_code)
    #     rcc_authors_fr = detail_page.localized.get_rcc_authors()

    #     self.assertEqual(len(rcc_authors_fr), 1)
    #     self.assertIn(profile_fr, rcc_authors_fr)
    #     self.assertNotIn(profile_en, rcc_authors_fr)

    # def test_get_rcc_authors_returns_localized_profiles_rendered(self) -> None:
    #     """
    #     Similar to the above, but these links get passed to routablepageurl in the template
    #     so we can be certain that they come out localized.
    #     """
    #     detail_page = detail_page_factory.RCCDetailPageFactory(parent=self.library_page)
    #     self.synchronize_tree()
    #     # Translating both the page and the rcc author profile.
    #     detail_page_fr = rcc_test_utils.translate_detail_page(detail_page, self.fr_locale)
    #     profile_fr = detail_page_fr.rcc_authors.first().author_profile
    #     translation.activate(self.fr_locale.language_code)
    #     author_index = authors_index.RCCAuthorsIndexPage.objects.first()
    #     fr_author_index = authors_index.RCCAuthorsIndexPage.objects.filter(locale=self.fr_locale).first()

    #     # Build a URL to check for in the response.
    #     # E.G, /fr/rcc/authors/1/name-here/
    #     fr_author_link = fr_author_index.url + fr_author_index.reverse_subpage(
    #         "wagtailpages:rcc-author-detail", kwargs={"profile_slug": profile_fr.slug}
    #     )
    #     en_author_link = author_index.url + author_index.reverse_subpage(
    #         "wagtailpages:rcc-author-detail", kwargs={"profile_slug": profile_fr.slug}
    #     )

    #     # Request the fr version of the page.
    #     response = self.client.get(detail_page_fr.url)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, fr_author_link)
    #     self.assertNotContains(response, en_author_link)

    # def test_get_rcc_authors_returns_default_locale(self) -> None:
    #     """
    #     If a related rcc author's profile does not have a translated version available,
    #     localized pages should return it in the default locale (English).
    #     """
    #     detail_page = detail_page_factory.RCCDetailPageFactory(
    #         parent=self.library_page,
    #     )
    #     profile_en = detail_page.rcc_authors.first().author_profile
    #     self.synchronize_tree()

    #     translation.activate(self.fr_locale.language_code)
    #     rcc_authors_fr = detail_page.localized.get_rcc_authors()

    #     self.assertEqual(len(rcc_authors_fr), 1)
    #     self.assertIn(profile_en, rcc_authors_fr)
