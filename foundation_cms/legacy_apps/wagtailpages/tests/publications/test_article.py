import http

from foundation_cms.legacy_apps.wagtailpages.factory import (
    publication as publication_factory,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.publications import article
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base


class ArticePageTests(test_base.WagtailpagesTestCase):
    def test_factory(self):
        publication_factory.ArticlePageFactory()

        self.assertTrue(True)

    def test_page_loads(self):
        artice_page = publication_factory.ArticlePageFactory(parent=self.homepage)

        response = self.client.get(path=artice_page.get_url())

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, artice_page.title)
        self.assertTemplateUsed("fragments/publication_hero.html")

    def test_page_loads_full_screen_hero(self):
        artice_page = publication_factory.ArticlePageFactory(
            parent=self.homepage,
            hero_layout=article.PublicationPage.HERO_LAYOUT_FULL_SCREEN,
        )

        response = self.client.get(path=artice_page.get_url())

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed("fragments/custom_hero.html")
        self.assertTemplateNotUsed("fragments/publication_hero.html")
