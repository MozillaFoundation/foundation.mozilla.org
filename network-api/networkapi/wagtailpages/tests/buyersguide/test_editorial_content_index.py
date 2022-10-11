import contextlib
import datetime
from http import HTTPStatus
from typing import TYPE_CHECKING, Optional
from unittest import mock

import bs4
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

        cls.request_factory = test.RequestFactory()

    def create_request(self, data: Optional[dict] = None) -> 'wsgi.WSGIRequest':
        return self.request_factory.get(path=self.content_index.url, data=data)

    def create_days_old_article(self, days: int):
        return buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
            first_published_at=timezone.now() - datetime.timedelta(days=days),
        )

    @contextlib.contextmanager
    def setup_content_index_with_pages_of_children(self):
        """
        Context manager setting up the content index with child pages.

        This is implemented as a context manager to allow us to mock / override the
        `items_per_page` attribute on the content index regardless of how often the
        page instance is created. This is important for integration tests with the
        Django test client, because the instance of the content index you set up with
        the factory is not the same that the client is hitting. A new instance is
        instantiated with the data from the datbase. Since `items_per_page` is not
        saved in the database it would be different on that instance. Mocking allows
        us to set a value we want to use for the test.

        Use this is in a with statement. The generated child pages are bound to the
        name after `as`.

        """
        self.items_per_page = 3
        with mock.patch('networkapi.wagtailpages.models.BuyersGuideEditorialContentIndexPage.items_per_page', 3):
            self.content_index.items_per_page = self.items_per_page
            articles = []
            # Create 2 more items then fit on page to check they are not in the page
            for days_old in range(self.items_per_page + 2):
                articles.append(self.create_days_old_article(days_old))
            yield articles

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

    def test_serve_paginated_items_page_1(self):
        with self.setup_content_index_with_pages_of_children() as articles:

            response = self.client.get(self.content_index.url)

            self.assertQuerysetEqual(
                response.context['items'],
                articles[:self.items_per_page],
            )

    def test_serve_paginated_items_page_2(self):
        with self.setup_content_index_with_pages_of_children() as articles:

            response = self.client.get(self.content_index.url, data={'page': 2})

            self.assertQuerysetEqual(
                response.context['items'],
                articles[self.items_per_page:],
            )

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

    def test_items_route_show_load_more_button_immediately(self):
        with self.setup_content_index_with_pages_of_children():
            url = self.content_index.url + self.content_index.reverse_subpage('items')

            response = self.client.get(url)

            self.assertTrue(response.context['show_load_more_button_immediately'])
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            # No pagination element in markup
            self.assertEqual(soup.find_all(id='pagination'), [])
            # But the load more element
            self.assertNotEqual(soup.find_all(id='load-more'), [])


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

    def test_items_route_paginated_items_page_1(self):
        with self.setup_content_index_with_pages_of_children() as articles:
            url = self.content_index.url + self.content_index.reverse_subpage('items')

            response = self.client.get(url)

            self.assertQuerysetEqual(
                response.context['items'],
                articles[:self.items_per_page],
            )

    def test_items_route_paginated_items_page_2(self):
        with self.setup_content_index_with_pages_of_children() as articles:
            url = self.content_index.url + self.content_index.reverse_subpage('items')

            response = self.client.get(url, data={'page': 2})

            self.assertQuerysetEqual(
                response.context['items'],
                articles[self.items_per_page:],
            )

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
        with self.setup_content_index_with_pages_of_children() as articles:

            context = self.content_index.get_context(request=self.create_request())

            self.assertQuerysetEqual(context['items'], articles[:self.items_per_page])

    def test_get_context_paginated_items_page_2(self):
        with self.setup_content_index_with_pages_of_children() as articles:
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

