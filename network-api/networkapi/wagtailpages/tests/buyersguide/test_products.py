import unittest

import json

from django.test import TestCase
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from wagtail.snippets.views.snippets import get_snippet_edit_handler
from wagtail.tests.utils import form_data

from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.buyersguide.products import (
    ProductPageVotes,
    BuyersGuideProductCategory,
)
from networkapi.wagtailpages.tests.buyersguide.base import BuyersGuideTestMixin


class TestProductPage(BuyersGuideTestMixin):

    def setUp(self):
        super().setUp()
        if not hasattr(self.product_page.votes, 'get_votes'):
            votes = ProductPageVotes()
            votes.save()
            self.product_page.votes = votes
            self.product_page.save()

    def test_get_votes(self):
        product_page = self.product_page

        # Votes should be empty at this point.
        votes = product_page.votes.get_votes()
        self.assertEqual(votes, [0, 0, 0, 0, 0])
        self.assertEqual(len(votes), 5)

    def test_set_votes(self):
        product_page = self.product_page

        # Make sure votes are set and saved.
        product_page.votes.set_votes([1, 2, 3, 4, 5])
        votes = product_page.votes.get_votes()
        self.assertEqual(votes, [1, 2, 3, 4, 5])

        # Ensure there's always 5 value set.
        product_page.votes.set_votes([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(votes, [1, 2, 3, 4, 5])
        self.assertEqual(len(votes), 5)

    def test_total_vote_count(self):
        product_page = self.product_page

        product_page.votes.set_votes([5, 4, 3, 2, 1])
        total_vote_count = product_page.total_vote_count
        self.assertEqual(total_vote_count, 15)

        product_page.votes.set_votes([5, 5, 5, 5, 5])
        total_vote_count = product_page.total_vote_count
        self.assertEqual(total_vote_count, 25)

    def test_creepiness(self):
        product_page = self.product_page

        product_page.creepiness_value = 100
        product_page.save()
        self.assertEqual(product_page.creepiness_value, 100)

        product_page.votes.set_votes([5, 5, 5, 5, 5])
        self.assertEqual(product_page.total_vote_count, 25)

        creepiness = product_page.creepiness
        self.assertEqual(creepiness, 4)

        product_page.creepiness_value = 0
        product_page.votes.set_votes([0, 0, 0, 0, 0])
        creepiness = product_page.creepiness
        self.assertEqual(creepiness, 50)

    def test_get_voting_json(self):
        product_page = self.product_page

        product_page.creepiness_value = 60
        product_page.save()
        self.assertEqual(product_page.creepiness_value, 60)

        product_page.votes.set_votes([1, 2, 3, 4, 5])
        self.assertEqual(product_page.total_vote_count, 15)

        creepiness = product_page.creepiness
        self.assertEqual(creepiness, 4)

        total_vote_count = product_page.total_vote_count
        self.assertEqual(total_vote_count, 15)

        # votes = product_page.votes.get_votes()
        data = json.loads(product_page.get_voting_json)
        comparable_data = {
            'creepiness': {
                'vote_breakdown':  {
                    '0': 1,
                    '1': 2,
                    '2': 3,
                    '3': 4,
                    '4': 5,
                },
                'average': 4.0,
            },
            'total': 15,
        }
        self.assertDictEqual(data, comparable_data)

    def test_get_or_create_votes(self):
        product_page = self.product_page

        # Delete potential votes
        product_page.votes.delete()
        product_page.votes = None
        self.assertEqual(product_page.votes, None)

        product_page.save()
        votes = product_page.get_or_create_votes()
        self.assertEqual(votes, [0, 0, 0, 0, 0])

        self.assertTrue(hasattr(product_page.votes, 'set_votes'))

    def test_related_articles(self):
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

        related_articles = product_page.related_article_relations.related_items()

        self.assertEqual(len(related_articles), 3)
        self.assertQuerysetEqual(
            related_articles,
            [article2, article1, article3],
            ordered=True,
        )


@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class WagtailBuyersGuideVoteTest(APITestCase, BuyersGuideTestMixin):

    def test_successful_vote(self):
        product_page = self.product_page

        # Reset votes
        product_page.get_or_create_votes()
        product_page.votes.set_votes([0, 0, 0, 0, 0])

        response = self.client.post(product_page.url, {
            'value': 25,
        }, format='json')
        self.assertEqual(response.status_code, 200)

        product_page.refresh_from_db()

        votes = product_page.votes.get_votes()
        self.assertListEqual(votes, [0, 1, 0, 0, 0])
        self.assertEqual(product_page.total_vote_count, 1)
        self.assertEqual(product_page.creepiness_value, 25)

        response = self.client.post(product_page.url, {
            'value': 100,
        }, format='json')
        self.assertEqual(response.status_code, 200)

        product_page.refresh_from_db()

        votes = product_page.votes.get_votes()
        self.assertListEqual(votes, [0, 1, 0, 0, 1])
        self.assertEqual(product_page.total_vote_count, 2)
        self.assertEqual(product_page.creepiness_value, 125)

    def test_bad_vote_value(self):
        # vote = 500
        response = self.client.post(self.product_page.url, {
            'value': -1,
        }, format='json')
        self.assertEqual(response.status_code, 405)

        response = self.client.post(self.product_page.url, {
            'value': 101,
        }, format='json')
        self.assertEqual(response.status_code, 405)

    def test_vote_on_draft_page(self):
        self.product_page.live = False
        self.product_page.save()

        response = self.client.post(self.product_page.url, {
            'value': 25,
            'productID': self.product_page.id
        }, format='json')
        self.assertEqual(response.status_code, 404)

        # Reset the page back to Live
        self.product_page.live = True
        self.product_page.save()


class BuyersGuideProductCategoryTest(TestCase):

    def setUp(self):
        edit_handler = get_snippet_edit_handler(BuyersGuideProductCategory)
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
        return form_data.nested_form_data({
            **data,
            'related_article_relations': form_data.inline_formset([])
        })

    def test_cannot_have_duplicate_name(self):
        BuyersGuideProductCategory.objects.create(name="Cat 1")

        form = self.form_class(
            data=self.generate_form_data({'name': 'Cat 1', 'sort_order': 1}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn('name', form.errors)

    def test_cannot_have_duplicate_lowercase_name(self):
        BuyersGuideProductCategory.objects.create(name="Cat 1")

        form = self.form_class(
            data=self.generate_form_data({'name': 'cat 1', 'sort_order': 1}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn('name', form.errors)

    def test_parent_saves(self):
        cat1 = BuyersGuideProductCategory.objects.create(name="Cat 1")

        form = self.form_class(
            data=self.generate_form_data({
                'name': 'Cat 2',
                'sort_order': 1,
                'parent': cat1,
            }),
        )

        self.assertTrue(form.is_valid())
        cat2 = form.save()
        self.assertEqual(cat1, cat2.parent)

    def test_cannot_be_direct_child_of_itself(self):
        cat1 = BuyersGuideProductCategory.objects.create(name="Cat 1")

        form = self.form_class(
            instance=cat1,
            data=self.generate_form_data({
                'name': cat1.name,
                'sort_order': cat1.sort_order,
                'parent': cat1
            }),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn('parent', form.errors)
        self.assertIn(
            'A category cannot be a parent of itself.',
            form.errors['parent']
        )

    def test_cannot_be_created_more_than_two_levels_deep(self):
        cat1 = BuyersGuideProductCategory.objects.create(name="Cat 1")
        cat2 = BuyersGuideProductCategory.objects.create(name="Cat 2", parent=cat1)

        form = self.form_class(
            data=self.generate_form_data({
                'name': 'Cat 3',
                'sort_order': 1,
                'parent': cat2
            }),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn('parent', form.errors)
        self.assertIn(
            'Categories can only be two levels deep.',
            form.errors['parent']
        )

    def test_related_articles(self):
        cat = BuyersGuideProductCategory.objects.create(name="Test category")
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

        related_articles = cat.related_article_relations.related_items()

        self.assertEqual(len(related_articles), 3)
        self.assertQuerysetEqual(
            related_articles,
            [article2, article1, article3],
            ordered=True,
        )

    # TODO: Figure out why this test is failing
    @unittest.skip(
        'Though the category snippets seem to be working correctly in the CMS, '
        'this test appears to be failing as it is returning a duplicate article.'
        'We believe this is due to a wagtail-localize issue that is preventing '
        'these items from being translated, meaning a category is being used for '
        'two different localizations of the same page (e.g. English and French). '
        'See also: https://github.com/mozilla/foundation.mozilla.org/pull/9240'
        'and: https://github.com/wagtail/wagtail-localize/issues/591'
    )
    def test_related_articles_on_multiple_categories(self):
        cat1 = BuyersGuideProductCategory.objects.create(name="Cat 1")
        cat2 = BuyersGuideProductCategory.objects.create(name="Cat 2")
        article1 = buyersguide_factories.BuyersGuideArticlePageFactory()
        article2 = buyersguide_factories.BuyersGuideArticlePageFactory()
        article3 = buyersguide_factories.BuyersGuideArticlePageFactory()
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
            article=article2,
            sort_order=4,
        )

        cat1_related_articles = cat1.related_article_relations.related_items()
        cat2_related_articles = cat2.related_article_relations.related_items()

        self.assertEqual(len(cat1_related_articles), 3)
        self.assertQuerysetEqual(
            cat1_related_articles,
            [article2, article1, article3],
            ordered=True,
        )
        self.assertEqual(len(cat2_related_articles), 1)
        self.assertQuerysetEqual(
            cat2_related_articles,
            [article2],
            ordered=True,
        )
