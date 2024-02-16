import json

import bs4
from django.test import TestCase
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from wagtail.admin.panels import get_edit_handler
from wagtail.test.utils import form_data

from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.buyersguide.products import (
    BuyersGuideProductCategory,
    ProductPageCategory,
)
from networkapi.wagtailpages.tests.buyersguide.base import BuyersGuideTestCase


class TestProductPage(BuyersGuideTestCase):
    def setUp(self):
        super().setUp()
        self.product_page.evaluation = buyersguide_factories.ProductPageEvaluationFactory()
        self.product_page.save()
        self.login()

    def test_get_votes(self):
        product_page = self.product_page

        # Votes should be empty at this point.
        self.assertEqual(list(product_page.evaluation.votes.all()), [])

    def test_get_voting_json(self):
        product_page = self.product_page

        # Create votes:
        buyersguide_factories.ProductVoteFactory(value=10, evaluation=product_page.evaluation)

        for _ in range(2):
            buyersguide_factories.ProductVoteFactory(value=30, evaluation=product_page.evaluation)

        for _ in range(3):
            buyersguide_factories.ProductVoteFactory(value=50, evaluation=product_page.evaluation)

        for _ in range(4):
            buyersguide_factories.ProductVoteFactory(value=70, evaluation=product_page.evaluation)

        for _ in range(5):
            buyersguide_factories.ProductVoteFactory(value=90, evaluation=product_page.evaluation)

        product_page.refresh_from_db()
        evaluation = product_page.annotated_evaluation

        self.assertEqual(evaluation.total_creepiness, 950)
        self.assertEqual(product_page.total_vote_count, 15)
        self.assertAlmostEqual(product_page.creepiness, 950 / 15)

        # votes = product_page.votes.get_votes()
        data = json.loads(product_page.get_voting_json)
        comparable_data = {
            "creepiness": {
                "vote_breakdown": {
                    "0": 1,
                    "1": 2,
                    "2": 3,
                    "3": 4,
                    "4": 5,
                },
                "average": 950 / 15,
            },
            "total": 15,
        }
        self.assertDictEqual(data, comparable_data)

    def test_localized_related_products(self):
        product_page = self.product_page

        related_products = []
        for _ in range(10):
            related_product = buyersguide_factories.ProductPageFactory(parent=self.bg)
            buyersguide_factories.RelatedProductsFactory(
                page=product_page,
                related_product=related_product,
            )
            related_products.append(related_product)

        with self.assertNumQueries(4):
            result = product_page.localized_related_products
            for related_product in related_products:
                self.assertIn(related_product, result)

    def test_localized_related_products_non_default_locale(self):
        product_page = self.product_page

        first_product = buyersguide_factories.ProductPageFactory(parent=self.bg, title="First product")
        second_product = buyersguide_factories.ProductPageFactory(parent=self.bg, title="Second product")

        buyersguide_factories.RelatedProductsFactory(
            page=product_page,
            related_product=first_product,
        )
        buyersguide_factories.RelatedProductsFactory(
            page=product_page,
            related_product=second_product,
        )

        related_products_en = product_page.localized_related_products
        self.assertIn(first_product, related_products_en)
        self.assertIn(second_product, related_products_en)

        self.translate_page(product_page, self.fr_locale)
        fr_product_page = product_page.get_translation(self.fr_locale)

        self.translate_page(first_product, self.fr_locale)
        first_product_fr = first_product.get_translation(self.fr_locale)
        first_product_fr.title = "Premier produit"
        first_product_fr.save_revision().publish()

        self.activate_locale(self.fr_locale)

        related_products_fr = fr_product_page.localized_related_products
        # If there is a localized version, that should be returned:
        self.assertIn(first_product_fr, related_products_fr)
        # If there is no localized version, the default version should be returned:
        self.assertIn(second_product, related_products_fr)

    def test_preview_related_products(self):
        """
        Tests if `preview_related_products` returns related products according to sort order,
        and renders them in the ProductPage CMS preview panel.
        """
        product_page = self.product_page

        related_product_1 = buyersguide_factories.ProductPageFactory.build(parent=self.bg)
        related_product_2 = buyersguide_factories.ProductPageFactory.build(parent=self.bg)
        related_product_3 = buyersguide_factories.ProductPageFactory.build(parent=self.bg)

        product_relation_1 = buyersguide_factories.RelatedProductsFactory.build(
            page=product_page, related_product=related_product_1
        )
        product_relation_2 = buyersguide_factories.RelatedProductsFactory.build(
            page=product_page, related_product=related_product_2
        )
        product_relation_3 = buyersguide_factories.RelatedProductsFactory.build(
            page=product_page, related_product=related_product_3
        )

        # Setting related products in memory, but not yet saving to DB.
        product_page.related_product_pages = [product_relation_2, product_relation_1, product_relation_3]

        preview_methods_related_products = product_page.preview_related_products

        # Check if method returns related products as expected.
        # Order should be: product 2, product 1, product 3.
        self.assertListEqual(
            preview_methods_related_products,
            [related_product_2, related_product_1, related_product_3],
        )

        # Grab preview template response, find all related product titles in HTML.
        preview_response = product_page.make_preview_request()
        soup = bs4.BeautifulSoup(preview_response.content, "html.parser")
        related_product_titles_from_preview_template = [
            p.get_text(strip=True) for p in soup.find_all("p", class_="product-title")
        ]

        # Check if template renders related products as expected.
        # Order should be: product 2, product 1, product 3.
        self.assertEqual(
            related_product_titles_from_preview_template,
            [related_product_2.title, related_product_1.title, related_product_3.title],
        )

    def test_preview_related_products_after_deletion(self):
        """
        Tests if `preview_related_products` accurately returns related products for CMS page previews,
        even after a related product relation is deleted.
        """
        product_page = self.product_page

        related_product_1 = buyersguide_factories.ProductPageFactory.build(parent=self.bg)
        related_product_2 = buyersguide_factories.ProductPageFactory.build(parent=self.bg)
        related_product_3 = buyersguide_factories.ProductPageFactory.build(parent=self.bg)

        product_relation_1 = buyersguide_factories.RelatedProductsFactory.build(
            page=product_page,
            related_product=related_product_1,
        )
        product_relation_2 = buyersguide_factories.RelatedProductsFactory.build(
            page=product_page,
            related_product=related_product_2,
        )
        product_relation_3 = buyersguide_factories.RelatedProductsFactory.build(
            page=product_page,
            related_product=related_product_3,
        )

        # Setting related products in memory, but not yet saving to DB.
        product_page.related_product_pages = [product_relation_2, product_relation_1, product_relation_3]

        preview_methods_related_products = product_page.preview_related_products

        # Check if method returns related products as expected.
        # Order should be: product 2, product 1, product 3.
        self.assertListEqual(
            preview_methods_related_products,
            [related_product_2, related_product_1, related_product_3],
        )

        # Grab preview template response, find all related product titles in HTML.
        preview_response = product_page.make_preview_request()
        soup = bs4.BeautifulSoup(preview_response.content, "html.parser")
        related_product_titles_from_preview_template = [
            p.get_text(strip=True) for p in soup.find_all("p", class_="product-title")
        ]

        # Check if template returns related products as expected.
        # Order should be: product 2, product 1, product 3.
        self.assertEqual(
            related_product_titles_from_preview_template,
            [related_product_2.title, related_product_1.title, related_product_3.title],
        )

        # Remove one product relation.
        product_page.related_product_pages.remove(product_relation_1)

        # Fetch the related products again after modification.
        preview_methods_related_products_after_deletion = product_page.preview_related_products

        # Make sure list returned reflects the deletion.
        # Order should be product 2, product 3.
        self.assertListEqual(
            preview_methods_related_products_after_deletion,
            [related_product_2, related_product_3],
        )

        # Double check that preview template reflects deletion as expected.
        preview_response = product_page.make_preview_request()
        soup = bs4.BeautifulSoup(preview_response.content, "html.parser")
        related_product_titles_from_preview_template = [
            p.get_text(strip=True) for p in soup.find_all("p", class_="product-title")
        ]

        # Check if template reflects update.
        # Order should be: product 2, product 3.
        self.assertEqual(
            related_product_titles_from_preview_template, [related_product_2.title, related_product_3.title]
        )

    def test_preview_related_products_after_reorder(self):
        """
        Tests if `preview_related_products` accurately returns related products for CMS page previews,
        even after related products are reordered.
        """
        product_page = self.product_page

        related_product_1 = buyersguide_factories.ProductPageFactory.build(parent=self.bg)
        related_product_2 = buyersguide_factories.ProductPageFactory.build(parent=self.bg)
        related_product_3 = buyersguide_factories.ProductPageFactory.build(parent=self.bg)

        product_relation_1 = buyersguide_factories.RelatedProductsFactory.build(
            page=product_page,
            related_product=related_product_1,
        )
        product_relation_2 = buyersguide_factories.RelatedProductsFactory.build(
            page=product_page,
            related_product=related_product_2,
        )
        product_relation_3 = buyersguide_factories.RelatedProductsFactory.build(
            page=product_page,
            related_product=related_product_3,
        )

        # Setting related products in memory, but not yet saving to DB.
        product_page.related_product_pages = [product_relation_2, product_relation_1, product_relation_3]

        preview_methods_related_products = product_page.preview_related_products

        # Check if method returns related products as expected.
        # Order should be: product 2, product 1, product 3.
        self.assertListEqual(
            preview_methods_related_products,
            [related_product_2, related_product_1, related_product_3],
        )

        # Grab preview template response, find all related product titles in HTML.
        preview_response = product_page.make_preview_request()
        soup = bs4.BeautifulSoup(preview_response.content, "html.parser")
        related_product_titles_from_preview_template = [
            p.get_text(strip=True) for p in soup.find_all("p", class_="product-title")
        ]

        # Check if template renders related products as expected.
        # Order should be: product 2, product 1, product 3.
        self.assertEqual(
            related_product_titles_from_preview_template,
            [related_product_2.title, related_product_1.title, related_product_3.title],
        )

        # Update product order in memory.
        # New order is: product 3, product 2, product 1
        product_page.related_product_pages = [product_relation_3, product_relation_2, product_relation_1]

        # Fetch the related products again after modification.
        preview_methods_related_products_after_reorder = product_page.preview_related_products

        # Updated order should now be: product 3, product 2, product 1.
        self.assertListEqual(
            preview_methods_related_products_after_reorder,
            [related_product_3, related_product_2, related_product_1],
        )

        # Grab preview template response, find all related product titles in HTML.
        preview_response = product_page.make_preview_request()
        soup = bs4.BeautifulSoup(preview_response.content, "html.parser")
        related_product_titles_from_preview_template = [
            p.get_text(strip=True) for p in soup.find_all("p", class_="product-title")
        ]

        # Check if template reflects update.
        # Order should be: product 3, product 2, product 1.
        self.assertEqual(
            related_product_titles_from_preview_template,
            [related_product_3.title, related_product_2.title, related_product_1.title],
        )

    def test_preview_related_products_with_no_products(self):
        """
        Tests if `preview_related_products` returns an empty list if no related products are set.
        """
        product_page = self.product_page

        related_preview_products = product_page.preview_related_products

        self.assertEqual(related_preview_products, [])

    def test_get_related_articles(self):
        """
        Returns all related articles.

        We don't want the through model, we really want the articles.
        """
        product_page = self.product_page

        related_articles = []
        for _ in range(5):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory()
            buyersguide_factories.BuyersGuideProductPageArticlePageRelationFactory(
                product=product_page,
                article=related_article,
            )
            related_articles.append(related_article)

        result = product_page.get_related_articles()

        for related_article in related_articles:
            self.assertIn(related_article, result)

    def test_get_related_articles_non_default_locale(self):
        """
        Returns all related articles localized.
        """
        content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=self.bg,
        )
        product_page = self.product_page
        related_articles_en = []
        for _ in range(5):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory(parent=content_index)
            buyersguide_factories.BuyersGuideProductPageArticlePageRelationFactory(
                product=product_page,
                article=related_article,
            )
            related_articles_en.append(related_article)
        self.synchronize_tree()
        related_articles_fr = []
        for article in related_articles_en:
            article_fr = article.get_translation(self.fr_locale)
            related_articles_fr.append(article_fr)

        product_page_fr = product_page.get_translation(self.fr_locale)
        self.activate_locale(self.fr_locale)
        results_fr = product_page_fr.get_related_articles()

        for related_article in results_fr:
            self.assertIn(related_article, related_articles_fr)

    def test_get_related_articles_no_related_articles(self):
        product_page = self.product_page

        result = product_page.get_related_articles()

        self.assertListEqual(result, [])

    def test_get_related_articles_order(self):
        product_page = self.product_page
        article1 = buyersguide_factories.BuyersGuideArticlePageFactory()
        article2 = buyersguide_factories.BuyersGuideArticlePageFactory()
        article3 = buyersguide_factories.BuyersGuideArticlePageFactory()
        buyersguide_factories.BuyersGuideProductPageArticlePageRelationFactory(
            product=product_page,
            article=article2,
            sort_order=0,
        )
        buyersguide_factories.BuyersGuideProductPageArticlePageRelationFactory(
            product=product_page,
            article=article1,
            sort_order=1,
        )
        buyersguide_factories.BuyersGuideProductPageArticlePageRelationFactory(
            product=product_page,
            article=article3,
            sort_order=2,
        )

        related_articles = product_page.get_related_articles()

        self.assertEqual(len(related_articles), 3)
        self.assertListEqual(
            related_articles,
            [article2, article1, article3],
        )

    def test_primary_related_articles(self):
        """First three related articles are primary."""
        product_page = self.product_page

        related_articles = []
        for i in range(5):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory()
            buyersguide_factories.BuyersGuideProductPageArticlePageRelationFactory(
                product=product_page,
                article=related_article,
                sort_order=i,
            )
            related_articles.append(related_article)

        result = product_page.get_primary_related_articles()

        for related_article in related_articles[:3]:
            self.assertIn(related_article, result)
        for related_article in related_articles[3:]:
            self.assertNotIn(related_article, result)

    def test_primary_related_articles_non_default_locale(self):
        """First three related articles are primary and should be returned localized."""
        content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=self.bg,
        )
        product_page = self.product_page
        related_articles_en = []
        for i in range(5):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory(parent=content_index)
            buyersguide_factories.BuyersGuideProductPageArticlePageRelationFactory(
                product=product_page,
                article=related_article,
                sort_order=i,
            )
            related_articles_en.append(related_article)
        self.synchronize_tree()
        related_articles_fr = []
        for article in related_articles_en:
            article_fr = article.get_translation(self.fr_locale)
            related_articles_fr.append(article_fr)

        product_page_fr = product_page.get_translation(self.fr_locale)
        self.activate_locale(self.fr_locale)
        result = product_page_fr.get_primary_related_articles()

        for related_article in related_articles_fr[:3]:
            self.assertIn(related_article, result)
        for related_article in related_articles_fr[3:]:
            self.assertNotIn(related_article, result)

    def test_primary_related_articles_no_related_articles(self):
        product_page = self.product_page

        result = product_page.get_primary_related_articles()

        self.assertListEqual(result, [])

    def test_secondary_related_articles(self):
        """Second three related articles are secondary."""
        product_page = self.product_page

        related_articles = []
        for i in range(5):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory()
            buyersguide_factories.BuyersGuideProductPageArticlePageRelationFactory(
                product=product_page,
                article=related_article,
                sort_order=i,
            )
            related_articles.append(related_article)

        result = product_page.get_secondary_related_articles()

        for related_article in related_articles[:3]:
            self.assertNotIn(related_article, result)
        for related_article in related_articles[3:]:
            self.assertIn(related_article, result)

    def test_secondary_related_articles_non_default_locale(self):
        """Second three related articles are secondary and should be returned localized."""
        content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=self.bg,
        )
        product_page = self.product_page
        related_articles_en = []
        for i in range(5):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory(parent=content_index)
            buyersguide_factories.BuyersGuideProductPageArticlePageRelationFactory(
                product=product_page,
                article=related_article,
                sort_order=i,
            )
            related_articles_en.append(related_article)
        self.synchronize_tree()
        related_articles_fr = []
        for article in related_articles_en:
            article_fr = article.get_translation(self.fr_locale)
            related_articles_fr.append(article_fr)

        product_page_fr = product_page.get_translation(self.fr_locale)
        self.activate_locale(self.fr_locale)
        result = product_page_fr.get_secondary_related_articles()

        for related_article in related_articles_fr[:3]:
            self.assertNotIn(related_article, result)
        for related_article in related_articles_fr[3:]:
            self.assertIn(related_article, result)

    def test_secondary_related_articles_no_related_articles(self):
        product_page = self.product_page

        result = product_page.get_secondary_related_articles()

        self.assertListEqual(result, [])

    def test_product_with_single_enabled_category_shows_cta(self):
        """
        Testing that a product with an assigned category that has
        show_cta=True returns the CTA in context as expected.
        """
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.bg.call_to_action = cta
        self.bg.save()

        product_page = self.product_page

        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1", show_cta=True)
        category_orderable_1 = ProductPageCategory(
            product=product_page,
            category=cat1,
        )
        category_orderable_1.save()

        self.product_page.product_categories.add(category_orderable_1)
        self.product_page.save_revision().publish()

        response = self.client.get(product_page.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cta, response.context["featured_cta"])

    def test_product_with_single_disabled_category_hides_cta(self):
        """
        Testing that a product with an assigned category that has
        show_cta=False does not return the CTA in context as expected.
        """
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.bg.call_to_action = cta
        self.bg.save()

        product_page = self.product_page

        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1", show_cta=False)
        category_orderable_1 = ProductPageCategory(
            product=product_page,
            category=cat1,
        )
        category_orderable_1.save()

        self.product_page.product_categories.add(category_orderable_1)
        self.product_page.save_revision().publish()

        response = self.client.get(product_page.url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["featured_cta"])

    def test_product_with_multiple_categories_shows_cta(self):
        """
        Testing that a product with any assigned category that has
        show_cta=True returns the CTA in context as expected.
        """
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.bg.call_to_action = cta
        self.bg.save()

        product_page = self.product_page

        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1", show_cta=True)
        cat2 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 2", show_cta=False)
        category_orderable_1 = ProductPageCategory(
            product=product_page,
            category=cat1,
        )
        category_orderable_2 = ProductPageCategory(
            product=product_page,
            category=cat2,
        )
        category_orderable_1.save()
        category_orderable_2.save()

        self.product_page.product_categories.add(category_orderable_1)
        self.product_page.product_categories.add(category_orderable_2)
        self.product_page.save_revision().publish()

        response = self.client.get(product_page.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cta, response.context["featured_cta"])

    def test_product_with_multiple_categories_hides_cta(self):
        """
        Testing that a product where no assigned categories have show_cta=True
        does not return the CTA in context as expected.
        """
        product_page = self.product_page

        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1", show_cta=False)
        cat2 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 2", show_cta=False)
        category_orderable_1 = ProductPageCategory(
            product=product_page,
            category=cat1,
        )
        category_orderable_2 = ProductPageCategory(
            product=product_page,
            category=cat2,
        )
        category_orderable_1.save()
        category_orderable_2.save()

        self.product_page.product_categories.add(category_orderable_1)
        self.product_page.product_categories.add(category_orderable_2)
        self.product_page.save_revision().publish()

        response = self.client.get(product_page.url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["featured_cta"])

    def test_get_featured_cta_with_single_category_returns_cta(self):
        """
        Testing the product page's get_featured_cta function with
        a single category. If it has show_cta=True,
        this function should return the CTA object.
        """
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.bg.call_to_action = cta
        self.bg.save()

        product_page = self.product_page

        cat_with_cta_enabled = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1", show_cta=True)
        category_orderable_1 = ProductPageCategory(
            product=product_page,
            category=cat_with_cta_enabled,
        )
        category_orderable_1.save()
        self.product_page.product_categories.add(category_orderable_1)
        self.product_page.save_revision().publish()

        self.assertEqual(cta, product_page.get_featured_cta())

    def test_get_featured_cta_with_single_category_returns_none(self):
        """
        Testing the product page's get_featured_cta function with
        a single category. If it has show_cta=False,
        this function should return None.
        """
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.bg.call_to_action = cta
        self.bg.save()

        product_page = self.product_page

        cat_with_cta_disabled = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1", show_cta=False)
        category_orderable_1 = ProductPageCategory(
            product=product_page,
            category=cat_with_cta_disabled,
        )
        category_orderable_1.save()
        self.product_page.product_categories.add(category_orderable_1)
        self.product_page.save_revision().publish()

        self.assertEqual(None, product_page.get_featured_cta())

    def test_get_featured_cta_with_multiple_categories_returns_cta(self):
        """
        Testing the product page's get_featured_cta function with
        multiple categories. If one of the categories has show_cta=True,
        this function should return the CTA object.
        """
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.bg.call_to_action = cta
        self.bg.save()

        product_page = self.product_page

        cat_with_cta_enabled = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1", show_cta=True)
        cat_with_cta_disabled = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 2", show_cta=False)
        category_orderable_1 = ProductPageCategory(
            product=product_page,
            category=cat_with_cta_enabled,
        )
        category_orderable_1.save()
        category_orderable_2 = ProductPageCategory(
            product=product_page,
            category=cat_with_cta_disabled,
        )
        category_orderable_2.save()
        self.product_page.product_categories.add(category_orderable_1)
        self.product_page.product_categories.add(category_orderable_2)
        self.product_page.save_revision().publish()

        self.assertEqual(cta, product_page.get_featured_cta())

    def test_get_featured_cta_with_multiple_categories_returns_none(self):
        """
        Testing the product page's get_featured_cta function with
        multiple categories. If none of the categories have show_cta=True,
        this function should return None.
        """
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.bg.call_to_action = cta
        self.bg.save()

        product_page = self.product_page

        cat_with_cta_disabled_1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1", show_cta=False)
        cat_with_cta_disabled_2 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 2", show_cta=False)
        category_orderable_1 = ProductPageCategory(
            product=product_page,
            category=cat_with_cta_disabled_1,
        )
        category_orderable_1.save()
        category_orderable_2 = ProductPageCategory(
            product=product_page,
            category=cat_with_cta_disabled_2,
        )
        category_orderable_2.save()
        self.product_page.product_categories.add(category_orderable_1)
        self.product_page.product_categories.add(category_orderable_2)
        self.product_page.save_revision().publish()

        self.assertEqual(None, product_page.get_featured_cta())


@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class WagtailBuyersGuideVoteTest(APITestCase, BuyersGuideTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.admin_user = self.create_superuser(username="admin", password="password")
        self.login(self.admin_user)

    def test_successful_vote(self):
        product_page = self.product_page
        # Reset votes
        product_page.evaluation = buyersguide_factories.ProductPageEvaluationFactory()
        product_page.save()

        response = self.client.post(
            product_page.url,
            {
                "value": 25,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        product_page.refresh_from_db()
        evaluation = product_page.annotated_evaluation

        self.assertEqual(evaluation.total_votes, 1)
        self.assertEqual(evaluation.total_creepiness, 25)
        self.assertEqual(evaluation.average_creepiness, 25)
        self.assertEqual(product_page.total_vote_count, 1)
        self.assertEqual(product_page.creepiness, 25)

        response = self.client.post(
            product_page.url,
            {
                "value": 99,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        product_page.refresh_from_db()
        evaluation = product_page.annotated_evaluation

        self.assertEqual(evaluation.total_votes, 2)
        self.assertEqual(evaluation.total_creepiness, 124)
        self.assertEqual(evaluation.average_creepiness, 62)
        self.assertEqual(product_page.total_vote_count, 2)
        self.assertEqual(product_page.creepiness, 62)

    def test_successful_vote_on_translated_page(self):
        product_page = self.product_page
        # Reset votes
        product_page.evaluation = buyersguide_factories.ProductPageEvaluationFactory()
        product_page.save()

        self.translate_page(self.homepage, self.fr_locale)
        self.translate_page(self.bg, self.fr_locale)
        self.translate_page(product_page, self.fr_locale)
        fr_product_page = product_page.get_translation(self.fr_locale)

        response = self.client.post(
            fr_product_page.url,
            {
                "value": 25,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        fr_product_page.refresh_from_db()
        fr_evaluation = fr_product_page.annotated_evaluation

        self.assertEqual(fr_evaluation.total_votes, 1)
        self.assertEqual(fr_evaluation.total_creepiness, 25)
        self.assertEqual(fr_evaluation.average_creepiness, 25)
        self.assertEqual(fr_product_page.total_vote_count, 1)
        self.assertEqual(fr_product_page.creepiness, 25)

        # Although the vote was in the French locale, the pages share the same evaluation
        # so the data should be the same:

        product_page.refresh_from_db()
        evaluation = product_page.annotated_evaluation

        self.assertEqual(evaluation.total_votes, 1)
        self.assertEqual(evaluation.total_creepiness, 25)
        self.assertEqual(evaluation.average_creepiness, 25)
        self.assertEqual(product_page.total_vote_count, 1)
        self.assertEqual(product_page.creepiness, 25)

        response = self.client.post(
            product_page.url,
            {
                "value": 99,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        product_page.refresh_from_db()
        evaluation = product_page.annotated_evaluation

        self.assertEqual(evaluation.total_votes, 2)
        self.assertEqual(evaluation.total_creepiness, 124)
        self.assertEqual(evaluation.average_creepiness, 62)
        self.assertEqual(product_page.total_vote_count, 2)
        self.assertEqual(product_page.creepiness, 62)

        fr_product_page.refresh_from_db()
        fr_evaluation = fr_product_page.annotated_evaluation

        self.assertEqual(fr_evaluation.total_votes, 2)
        self.assertEqual(fr_evaluation.total_creepiness, 124)
        self.assertEqual(fr_evaluation.average_creepiness, 62)
        self.assertEqual(fr_product_page.total_vote_count, 2)
        self.assertEqual(fr_product_page.creepiness, 62)

    def test_bad_vote_value(self):
        # vote = 500
        response = self.client.post(
            self.product_page.url,
            {
                "value": -1,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 405)

        response = self.client.post(
            self.product_page.url,
            {
                "value": 101,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 405)

    def test_vote_on_draft_page(self):
        self.product_page.live = False
        self.product_page.save()

        response = self.client.post(
            self.product_page.url,
            {"value": 25, "productID": self.product_page.id},
            format="json",
        )
        self.assertEqual(response.status_code, 404)

        # Reset the page back to Live
        self.product_page.live = True
        self.product_page.save()


class BuyersGuideProductCategoryTest(TestCase):
    def setUp(self):
        edit_handler = get_edit_handler(BuyersGuideProductCategory)
        self.form_class = edit_handler.get_form_class()

    @staticmethod
    def generate_form_data(data: dict) -> dict:
        """
        Generate a valid from data for the product category form.

        Because of the inline panel for the related articles, we need to provide all
        the fields for those forms too. That would be quite tedious to do manually,
        especically since we are not testing that part of the form. Luckily, Wagtail
        provides some test helper function to generate this valid form data. This method
        is an extra wrapper around Wagtails helpers that allows to only specify the
        fields that we are interested in testing.
        """
        return form_data.nested_form_data({**data, "related_article_relations": form_data.inline_formset([])})

    def test_cannot_have_duplicate_name(self):
        buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")

        form = self.form_class(
            data=self.generate_form_data({"name": "Cat 1", "sort_order": 1}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("name", form.errors)

    def test_cannot_have_duplicate_lowercase_name(self):
        buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")

        form = self.form_class(
            data=self.generate_form_data({"name": "cat 1", "sort_order": 1}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("name", form.errors)

    def test_parent_saves(self):
        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")

        form = self.form_class(
            data=self.generate_form_data(
                {
                    "name": "Cat 2",
                    "sort_order": 1,
                    "parent": cat1,
                }
            ),
        )

        self.assertTrue(form.is_valid())
        cat2 = form.save()
        self.assertEqual(cat1, cat2.parent)

    def test_cannot_be_direct_child_of_itself(self):
        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")

        form = self.form_class(
            instance=cat1,
            data=self.generate_form_data({"name": cat1.name, "sort_order": cat1.sort_order, "parent": cat1}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("parent", form.errors)
        self.assertIn("A category cannot be a parent of itself.", form.errors["parent"])

    def test_cannot_be_created_more_than_two_levels_deep(self):
        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")
        cat2 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 2", parent=cat1)

        form = self.form_class(
            data=self.generate_form_data({"name": "Cat 3", "sort_order": 1, "parent": cat2}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("parent", form.errors)
        self.assertIn("Categories can only be two levels deep.", form.errors["parent"])

    def test_get_related_articles(self):
        """
        Returns all related articles.

        We don't want the through model, we really want the articles.
        """
        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")

        related_articles = []
        for _ in range(6):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory()
            buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
                category=cat1,
                article=related_article,
            )
            related_articles.append(related_article)

        result = cat1.get_related_articles()

        for related_article in related_articles:
            self.assertIn(related_article, result)

    def test_get_related_articles_no_related_articles(self):
        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")

        result = cat1.get_related_articles()

        self.assertListEqual(result, [])

    def test_get_related_articles_order(self):
        cat = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Test category")
        article1 = buyersguide_factories.BuyersGuideArticlePageFactory()
        article2 = buyersguide_factories.BuyersGuideArticlePageFactory()
        article3 = buyersguide_factories.BuyersGuideArticlePageFactory()
        buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
            category=cat,
            article=article2,
            sort_order=0,
        )
        buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
            category=cat,
            article=article1,
            sort_order=1,
        )
        buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
            category=cat,
            article=article3,
            sort_order=2,
        )

        related_articles = cat.get_related_articles()

        self.assertEqual(len(related_articles), 3)
        self.assertListEqual(
            related_articles,
            [article2, article1, article3],
        )

    def test_primary_related_articles(self):
        """First three related articles are primary."""
        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")

        related_articles = []
        for i in range(6):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory()
            buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
                category=cat1,
                article=related_article,
                sort_order=i,
            )
            related_articles.append(related_article)

        result = cat1.get_primary_related_articles()

        for related_article in related_articles[:3]:
            self.assertIn(related_article, result)
        for related_article in related_articles[3:]:
            self.assertNotIn(related_article, result)

    def test_primary_related_articles_no_related_articles(self):
        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")

        result = cat1.get_primary_related_articles()

        self.assertListEqual(result, [])

    def test_secondary_related_articles(self):
        """Second three related articles are secondary."""
        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")

        related_articles = []
        for i in range(6):
            related_article = buyersguide_factories.BuyersGuideArticlePageFactory()
            buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
                category=cat1,
                article=related_article,
                sort_order=i,
            )
            related_articles.append(related_article)

        result = cat1.get_secondary_related_articles()

        for related_article in related_articles[:3]:
            self.assertNotIn(related_article, result)
        for related_article in related_articles[3:]:
            self.assertIn(related_article, result)

    def test_secondary_related_articles_no_related_articles(self):
        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")

        result = cat1.get_secondary_related_articles()

        self.assertListEqual(result, [])

    def test_related_articles_on_multiple_categories(self):
        """
        Make sure articles can be related to multiple categories.

        During development I was running into issue with the OrderableRelationQuerySet
        where the related items would contains items multiple times.
        """
        cat1 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 1")
        cat2 = buyersguide_factories.BuyersGuideProductCategoryFactory(name="Cat 2")
        article1 = buyersguide_factories.BuyersGuideArticlePageFactory()
        article2 = buyersguide_factories.BuyersGuideArticlePageFactory()
        article3 = buyersguide_factories.BuyersGuideArticlePageFactory()
        article4 = buyersguide_factories.BuyersGuideArticlePageFactory()
        buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
            category=cat1,
            article=article2,
            sort_order=0,
        )
        buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
            category=cat1,
            article=article1,
            sort_order=1,
        )
        buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
            category=cat1,
            article=article3,
            sort_order=2,
        )
        buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
            category=cat2,
            article=article1,
            sort_order=0,
        )
        buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
            category=cat2,
            article=article3,
            sort_order=1,
        )
        buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
            category=cat2,
            article=article4,
            sort_order=2,
        )
        buyersguide_factories.BuyersGuideProductCategoryArticlePageRelationFactory(
            category=cat2,
            article=article2,
            sort_order=3,
        )

        with self.assertNumQueries(num=1):
            cat1_related_articles = cat1.get_related_articles()
        with self.assertNumQueries(num=1):
            cat2_related_articles = cat2.get_related_articles()

        self.assertEqual(len(cat1_related_articles), 3)
        self.assertListEqual(
            cat1_related_articles,
            [article2, article1, article3],
        )
        self.assertEqual(len(cat2_related_articles), 4)
        self.assertListEqual(
            cat2_related_articles,
            [article1, article3, article4, article2],
        )
