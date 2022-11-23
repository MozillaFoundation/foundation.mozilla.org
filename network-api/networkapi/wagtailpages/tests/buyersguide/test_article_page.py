from http import HTTPStatus

from wagtail.tests.utils.form_data import nested_form_data, streamfield, rich_text

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
        edit_handler = pagemodels.BuyersGuideArticlePage.get_edit_handler()
        cls.article_page_form = edit_handler.get_form_class()

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
            template_name="pages/buyersguide/article_page.html",
        )
        self.assertTemplateUsed(
            response=response,
            template_name="pages/buyersguide/base.html",
        )
        self.assertTemplateUsed(
            response=response,
            template_name="pages/base.html",
        )

    def test_content_template(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )

        response = self.client.get(article_page.url)

        self.assertTemplateUsed(
            response=response,
            template_name="wagtailpages/blocks/rich_text_block.html",
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

    def test_get_related_articles_no_related_articles(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )

        result = article_page.get_related_articles()

        self.assertListEqual(result, [])

    def test_related_articles_with_non_default_locale(self):
        """
        Related articles should be of same locale as the page itself.

        The relation is synchronized from the default locale, but when retrieved from
        the version of the non-default locale the related articles should be of that
        same non-default locale.
        """
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )
        related_article = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )
        buyersguide_factories.BuyersGuideArticlePageRelatedArticleRelationFactory(
            page=article_page,
            article=related_article,
        )
        self.synchronize_tree()
        article_page_fr = article_page.get_translation(self.fr_locale)
        related_article_fr = related_article.get_translation(self.fr_locale)
        self.activate_locale(self.fr_locale)

        related_articles_fr = article_page_fr.get_related_articles()

        self.assertIn(related_article_fr, related_articles_fr)

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

        self.assertListEqual(result, [])

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

    def test_secondary_related_articles_no_related_articles(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )

        result = article_page.get_secondary_related_articles()

        self.assertListEqual(result, [])

    @staticmethod
    def generate_form_data(data: dict) -> dict:
        """
        Generate valid form data for the BuyersGuide article page.

        We add the extra fields below to the dict as all these fields are set as
        required, and the form will return a validation error against them if left out.

        Since we have the "body" field set as required, we need to submit at least
        one StreamField in the form, or else the form will return a validation error.
        """
        return nested_form_data(
            {
                **data,
                "body": streamfield([("paragraph", rich_text("Hello world!"))]),
            }
        )

    def test_article_page_requires_search_image(self):
        """
        Test that the buyersguide article page form will
        return a validation error if no "search_image" is set.
        """
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(parent=self.content_index)

        test_form = self.article_page_form(
            instance=article_page,
            data=self.generate_form_data(
                {
                    "title": article_page.title,
                    "slug": article_page.slug,
                    "search_description": article_page.search_description,
                    "search_image": None,
                }
            ),
        )

        self.assertEqual(1, len(test_form.errors))
        self.assertIn("search_image", test_form.errors)
        self.assertIn("This field is required.", test_form.errors["search_image"])

    def test_article_page_requires_search_description(self):
        """
        Test that the buyersguide article page form will
        return a validation error if no "search_description" is set.
        """
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(parent=self.content_index)

        test_form = self.article_page_form(
            instance=article_page,
            data=self.generate_form_data(
                {
                    "title": article_page.title,
                    "slug": article_page.slug,
                    "search_description": None,
                    "search_image": article_page.search_image,
                }
            ),
        )

        self.assertEqual(1, len(test_form.errors))
        self.assertIn("search_description", test_form.errors)
        self.assertIn("This field is required.", test_form.errors["search_description"])

    def test_article_page_requires_both_search_fields(self):
        """
        Test that the buyersguide article page form will return validation
        errors for both "search_image" and "search_description" fields
        if neither are updated.
        """
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(parent=self.content_index)

        test_form = self.article_page_form(
            instance=article_page,
            data=self.generate_form_data(
                {
                    "title": article_page.title,
                    "slug": article_page.slug,
                    "search_description": None,
                    "search_image": None,
                }
            ),
        )

        self.assertEqual(2, len(test_form.errors))
        self.assertIn("search_image", test_form.errors)
        self.assertIn("search_description", test_form.errors)
        self.assertIn("This field is required.", test_form.errors["search_image"])
        self.assertIn("This field is required.", test_form.errors["search_description"])

    def test_article_page_with_search_fields_is_valid(self):
        """
        Test that a buyersguide article page form with
        the search fields set is valid with no errors.
        """
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(parent=self.content_index)

        test_form = self.article_page_form(
            instance=article_page,
            data=self.generate_form_data(
                {
                    "title": "New Test Title",
                    "slug": "new-test-title",
                    "search_description": article_page.search_description,
                    "search_image": article_page.search_image,
                }
            ),
        )

        self.assertEqual(0, len(test_form.errors))
