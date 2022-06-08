from http import HTTPStatus

from networkapi.wagtailpages.factory import blog as blog_factories
from networkapi.wagtailpages.tests import base as test_base


class TestBlogIndexSearch(test_base.WagtailpagesTestCase):
    def test_search_page(self):
        blog_index = blog_factories.BlogIndexPageFactory(parent=self.homepage)
        url = blog_index.get_url() + blog_index.reverse_subpage("search")

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
