from http import HTTPStatus

from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages import models as pagemodels
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories


class FactoriesTest(test_base.WagtailpagesTestCase):
    def test_page_factory(self):
        buyersguide_factories.BuyersGuideArticlePageFactory()

    def test_author_profile_relation_factory(self):
        buyersguide_factories.BuyersGuideArticlePageAuthorProfileRelationFactory()

    def test_content_category_relation_factory(self):
        buyersguide_factories.BuyersGuideArticlePageContentCategoryRelationFactory()

    def test_related_article_relation_factory(self):
        buyersguide_factories.BuyersGuideArticlePageRelatedArticleRelationFactory()


class BuyersGuideArticlePageTest(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.buyersguide_homepage = buyersguide_factories.BuyersGuidePageFactory(
            parent=cls.homepage,
        )
        cls.content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=cls.buyersguide_homepage,
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

    def test_buyersguide_home_page_in_context(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )

        response = self.client.get(article_page.url)

        self.assertEqual(response.context['home_page'], self.buyersguide_homepage)

    def test_content_template(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )

        response = self.client.get(article_page.url)

        self.assertTemplateUsed(
            response=response,
            template_name='wagtailpages/blocks/rich_text_block.html',
        )

    def test_get_related_articles(self):
        """
        Returns all related articles.

        We don't want the through model, we really want the articles.
        """
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )
        related_articles = []
        for _ in range(4):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory(
                parent=self.content_index,
            )
            buyersguide_factories.BuyersGuideArticlePageRelatedArticleRelationFactory(
                page=article_page,
                article=related_article,
            )
            related_articles.append(related_article)

        result = article_page.get_related_articles()

        for related_article in related_articles:
            self.assertIn(related_article, result)

    def test_related_article_relations_related_items(self):
        """
        Returns all related articles.

        We don't want the through model, we really want the articles.
        """
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )
        related_articles = []
        for _ in range(4):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory(
                parent=self.content_index,
            )
            buyersguide_factories.BuyersGuideArticlePageRelatedArticleRelationFactory(
                page=article_page,
                article=related_article,
            )
            related_articles.append(related_article)

        result = article_page.related_article_relations.related_items()

        for related_article in related_articles:
            self.assertIn(related_article, result)

    def test_get_related_articles_no_related_articles(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )

        result = article_page.get_related_articles()

        self.assertQuerysetEqual(result, [])

    def test_primary_related_articles(self):
        """First three related articles are primary."""
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )
        related_articles = []
        for _ in range(4):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory(
                parent=self.content_index,
            )
            buyersguide_factories.BuyersGuideArticlePageRelatedArticleRelationFactory(
                page=article_page,
                article=related_article,
            )
            related_articles.append(related_article)

        result = article_page.get_primary_related_articles()

        for related_article in related_articles[:3]:
            self.assertIn(related_article, result)
        self.assertNotIn(related_articles[-1], result)

    def test_primary_related_articles_no_related_articles(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )

        result = article_page.get_primary_related_articles()

        self.assertQuerysetEqual(result, [])

    def test_secondary_related_articles(self):
        """Second three related articles are secondary."""
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )
        related_articles = []
        for _ in range(6):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory(
                parent=self.content_index,
            )
            buyersguide_factories.BuyersGuideArticlePageRelatedArticleRelationFactory(
                page=article_page,
                article=related_article,
            )
            related_articles.append(related_article)

        result = article_page.get_secondary_related_articles()

        for related_article in related_articles[:3]:
            self.assertNotIn(related_article, result)
        for related_article in related_articles[3:]:
            self.assertIn(related_article, result)

    def test_secondary_related_articles_related_articles_no_related_articles(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )

        result = article_page.get_secondary_related_articles()

        self.assertQuerysetEqual(result, [])
