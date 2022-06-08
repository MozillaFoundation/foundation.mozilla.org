import datetime
from http import HTTPStatus

from networkapi.wagtailpages.factory import blog as blog_factories
from networkapi.wagtailpages.tests import base as test_base


class TestBlogIndexSearch(test_base.WagtailpagesTestCase):
    def test_route_success(self):
        blog_index = blog_factories.BlogIndexPageFactory(parent=self.homepage)
        url = blog_index.get_url() + blog_index.reverse_subpage("search")

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_no_query(self):
        blog_index = blog_factories.BlogIndexPageFactory(parent=self.homepage)
        tz = datetime.timezone.utc
        blog_page_1 = blog_factories.BlogPageFactory(
            parent=blog_index,
            first_published_at=datetime.datetime(2020, 1, 1, tzinfo=tz),
        )
        blog_page_2 = blog_factories.BlogPageFactory(
            parent=blog_index,
            first_published_at=datetime.datetime(2020, 1, 2, tzinfo=tz),
        )
        blog_page_3 = blog_factories.BlogPageFactory(
            parent=blog_index,
            first_published_at=datetime.datetime(2020, 1, 3, tzinfo=tz),
        )
        blog_page_4 = blog_factories.BlogPageFactory(
            parent=blog_index,
            first_published_at=datetime.datetime(2020, 1, 4, tzinfo=tz),
        )
        blog_page_5 = blog_factories.BlogPageFactory(
            parent=blog_index,
            first_published_at=datetime.datetime(2020, 1, 5, tzinfo=tz),
        )
        blog_page_6 = blog_factories.BlogPageFactory(
            parent=blog_index,
            first_published_at=datetime.datetime(2020, 1, 6, tzinfo=tz),
        )
        blog_page_7 = blog_factories.BlogPageFactory(
            parent=blog_index,
            first_published_at=datetime.datetime(2020, 1, 7, tzinfo=tz),
        )
        url = blog_index.get_url() + blog_index.reverse_subpage("search")

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        entries = response.context['entries'].specific()
        self.assertIn(blog_page_7, entries)
        self.assertIn(blog_page_6, entries)
        self.assertIn(blog_page_5, entries)
        self.assertIn(blog_page_4, entries)
        self.assertIn(blog_page_3, entries)
        self.assertIn(blog_page_2, entries)
        self.assertNotIn(blog_page_1, entries)
