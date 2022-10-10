import datetime
from http import HTTPStatus
from typing import TYPE_CHECKING, Optional

from django import test
from django.utils import timezone

from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages import models as pagemodels
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories

if TYPE_CHECKING:
    from django.core.handlers import wsgi


class BuyersGuideEditorialContentIndexPageFactoryTest(test_base.WagtailpagesTestCase):
    def test_factory(self):
        buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory()


class BuyersGuideEditorialContentIndexPageTest(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.pni_homepage = buyersguide_factories.BuyersGuidePageFactory(
            parent=cls.homepage,
        )
        cls.content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=cls.pni_homepage,
        )

    def create_request(self, data: Optional[dict] = None) -> 'wsgi.WSGIRequest':
        request_factory = test.RequestFactory()
        return request_factory.get(path=self.content_index.url, data=data)

    def create_days_old_article(self, days: int):
        return buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
            first_published_at=timezone.now() - datetime.timedelta(days=days),
        )

    def setup_content_index_with_pages_of_children(self):
        self.items_per_page = 3
        self.content_index.items_per_page = self.items_per_page
        articles = []
        # Create 2 more items then fit on page to check they are not in the page
        for days_old in range(self.items_per_page + 2):
            articles.append(self.create_days_old_article(days_old))
        return articles

    def test_parents(self):
        self.assertAllowedParentPageTypes(
            child_model=pagemodels.BuyersGuideEditorialContentIndexPage,
            parent_models={pagemodels.BuyersGuidePage},
        )

    def test_children(self):
        self.assertAllowedSubpageTypes(
            parent_model=pagemodels.BuyersGuideEditorialContentIndexPage,
            child_models={pagemodels.BuyersGuideArticlePage},
        )

    def test_page_success(self):
        response = self.client.get(self.content_index.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_templates_used(self):
        # Needs to use the client to test the templates
        response = self.client.get(self.content_index.url)

        self.assertTemplateUsed(
            response=response,
            template_name='pages/buyersguide/editorial_content_index_page.html',
        )
        self.assertTemplateUsed(
            response=response,
            template_name='pages/buyersguide/base.html',
        )
        self.assertTemplateUsed(
            response=response,
            template_name='pages/base.html',
        )

    def test_serve_shows_children_titles(self):
        children = []
        for _ in range(5):
            children.append(
                buyersguide_factories.BuyersGuideArticlePageFactory(
                    parent=self.content_index,
                )
            )

        response = self.client.get(path=self.content_index.url)

        for child in children:
            self.assertContains(response=response, text=child.title, count=1)

    def test_items_route_exists(self):
        route = self.content_index.reverse_subpage('items')

        self.assertEqual(route, 'items/')

    def test_items_route_template(self):
        url = self.content_index.url + self.content_index.reverse_subpage('items')

        response = self.client.get(url)

        self.assertTemplateUsed(
            response=response,
            template_name='fragments/buyersguide/editorial_content_index_items.html',
        )
        self.assertTemplateNotUsed(
            response=response,
            template_name='pages/buyersguide/editorial_content_index_page.html',
        )

    def test_items_route_shows_children_titles(self):
        url = self.content_index.url + self.content_index.reverse_subpage('items')
        children = []
        for _ in range(5):
            children.append(
                buyersguide_factories.BuyersGuideArticlePageFactory(
                    parent=self.content_index,
                )
            )

        response = self.client.get(path=url)

        for child in children:
            self.assertContains(response=response, text=child.title, count=1)

    def test_get_context_featured_cta(self):
        featured_cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.pni_homepage.call_to_action = featured_cta
        self.pni_homepage.save()

        context = self.content_index.get_context(request=self.create_request())

        self.assertEqual(context['featured_cta'], featured_cta)

    def test_get_context_no_cta_set_on_homepage(self):
        self.pni_homepage.call_to_action = None
        self.pni_homepage.save()

        context = self.content_index.get_context(request=self.create_request())

        self.assertIsNone(context['featured_cta'])

    def test_get_context_paginated_items_page_1(self):
        articles = self.setup_content_index_with_pages_of_children()

        context = self.content_index.get_context(request=self.create_request())

        self.assertQuerysetEqual(context['items'], articles[:self.items_per_page])

    def test_get_context_paginated_items_page_2(self):
        articles = self.setup_content_index_with_pages_of_children()
        request = self.create_request(data={'page': '2'})

        context = self.content_index.get_context(request=request)

        self.assertQuerysetEqual(context['items'], articles[self.items_per_page:])

    def test_get_items_ordered_by_publication_date(self):
        article_middle = self.create_days_old_article(days=10)
        article_oldest = self.create_days_old_article(days=20)
        article_newest = self.create_days_old_article(days=5)

        result = self.content_index.get_items()

        self.assertQuerysetEqual(
            qs=result,
            values=[
                article_newest,
                article_middle,
                article_oldest,
            ],
            ordered=True,
        )

    def test_get_related_articles(self):
        content_index = self.content_index
        article1 = buyersguide_factories.BuyersGuideArticlePageFactory()
        article2 = buyersguide_factories.BuyersGuideArticlePageFactory()
        article3 = buyersguide_factories.BuyersGuideArticlePageFactory()
        buyersguide_factories.BuyersGuideEditorialContentIndexPageArticlePageRelationFactory(
            page=content_index,
            article=article2,
            sort_order=0,
        )
        buyersguide_factories.BuyersGuideEditorialContentIndexPageArticlePageRelationFactory(
            page=content_index,
            article=article1,
            sort_order=1,
        )
        buyersguide_factories.BuyersGuideEditorialContentIndexPageArticlePageRelationFactory(
            page=content_index,
            article=article3,
            sort_order=2,
        )

        related_articles = content_index.get_related_articles()

        self.assertEqual(len(related_articles), 3)
        self.assertListEqual(
            related_articles,
            [article2, article1, article3],
        )

