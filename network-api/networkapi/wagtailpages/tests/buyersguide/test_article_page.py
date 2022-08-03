from http import HTTPStatus

from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages import models as pagemodels
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories


class FactoriesTest(test_base.WagtailpagesTestCase):
    def test_page_factory(self):
        buyersguide_factories.BuyersGuideArticlePageFactory()

    def test_author_factory(self):
        buyersguide_factories.BuyersGuideArticlePageAuthorFactory()

    def test_content_category_relation_factory(self):
        buyersguide_factories.BuyersGuideArticlePageContentCategoryRelationFactory()

    def test_content_category_relation_factory(self):
        buyersguide_factories.BuyersGuideArticlePageRelatedArticleFactory()


class BuyersGuideArticlePageTest(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.pni_homepage = buyersguide_factories.BuyersGuidePageFactory(
            parent=cls.homepage,
        )
        cls.content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=cls.pni_homepage,
        )

    def test_parents(self):
        self.assertAllowedParentPageTypes(
            child_model=pagemodels.BuyersGuideArticlePage,
            parent_models={pagemodels.BuyersGuideEditorialContentIndexPage},
        )

    def test_children(self):
        self.assertAllowedSubpageTypes(
            parent_model=pagemodels.BuyersGuideArticlePage,
            child_models={},
        )

    def test_page_success(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )

        response = self.client.get(article_page.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_template(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )

        response = self.client.get(article_page.url)

        self.assertTemplateUsed(
            response=response,
            template_name='pages/buyersguide/article_page.html',
        )
        self.assertTemplateUsed(
            response=response,
            template_name='pages/buyersguide/base.html',
        )
        self.assertTemplateUsed(
            response=response,
            template_name='pages/base.html',
        )

    def test_content_template(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )

        response = self.client.get(article_page.url)

        self.assertTemplateUsed(
            response=response,
            template_name='wagtailpages/blocks/rich_text_block.html',
        )

    # TODO: test splitting related articles into primary and secondary.
    def test_primary_related_articles(self):
        """First three related articles are primary."""
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )
        related_articles = []
        for _  in range(4):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory(
                parent=self.content_index,
            )
            buyersguide_factories.BuyersGuideArticlePageRelatedArticleFactory(
                page=article_page,
                article=related_article,
            )
            related_articles.append(related_article)

        primary_related_articles = article_page.get_primary_related_articles()

        for related_article in related_articles[:3]:
            self.assertIn(related_article, primary_related_articles)

        self.assertNotIn(related_articles[-1], primary_related_articles)


    def test_secondary_related_articles(self):
        """Second three related articles are secondary."""

    # TODO: test not enough related articles available.
