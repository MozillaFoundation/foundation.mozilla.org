import http

from django import test
from wagtail import models as wagtail_models

from networkapi.wagtailpages.factory import homepage as home_factory
from networkapi.wagtailpages.factory import blog as blog_factory



class TestBlogPage(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        root_node = wagtail_models.Page.get_first_root_node()
        site = wagtail_models.Site.objects.get(is_default_site=True)
        cls.homepage = home_factory.WagtailHomepageFactory(parent=root_node)
        site.root_page = cls.homepage
        site.clean()
        site.save()
        cls.blog_index = blog_factory.BlogIndexPageFactory(parent=cls.homepage)

    def test_page_loads(self):
        page = blog_factory.BlogPageFactory(parent=self.blog_index)

        response = self.client.get(page.url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

