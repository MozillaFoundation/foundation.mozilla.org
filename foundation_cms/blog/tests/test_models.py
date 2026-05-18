# from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.blog.factories import BlogIndexPageFactory, BlogPageFactory


class BlogPageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.blog_index = BlogIndexPageFactory()
        self.blog_page = BlogPageFactory(parent=self.blog_index)


class BlogIndexPageTestCase(WagtailPageTestCase):
    def setUp(self):
        """Set up a BlogIndexPage and attach BlogPages."""
        self.blog_index = BlogIndexPageFactory()
        self.blog_1 = BlogPageFactory(title="Blog 1", parent=self.blog_index)
        self.blog_2 = BlogPageFactory(title="Blog 2", parent=self.blog_index)

    def test_get_context(self):
        """This test ensures the context contains the correct number of blog pages."""
        request = self.client.get(self.blog_index.url)
        context = self.blog_index.get_context(request)

        self.assertEqual(len(context["blogs"]), 2)  # It ensures both blogs exist
        self.assertEqual(context["blogs"][0].title, self.blog_2.title)
