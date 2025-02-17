from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.profiles.models import Profile
from foundation_cms.profiles.factories import ProfileFactory
from foundation_cms.blog.factories import BlogPageFactory, BlogIndexPageFactory


class BlogPageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.blog_index = BlogIndexPageFactory()
        self.profile = ProfileFactory()
        self.blog_page = BlogPageFactory(parent=self.blog_index, author=self.profile)

    def test_default_route(self):
        """This test ensures the blog page is routable."""
        self.assertPageIsRoutable(self.blog_page)

    def test_author_name(self):
        """This test ensures author_name() returns a string and author is a Profile instance."""
        self.assertIsInstance(self.blog_page.author_name(), str)
        self.assertIsInstance(self.blog_page.author, Profile)
        self.assertEqual(self.blog_page.author, self.profile)

    def test_author_name_default(self):
        """If author is None, author_name() should return 'Mozilla Foundation'."""
        setattr(self.blog_page, "author", None)
        self.blog_page.save()
        self.assertEqual(self.blog_page.author_name(), "Mozilla Foundation")


class BlogIndexPageTestCase(WagtailPageTestCase):
    def setUp(self):
        """Set up a BlogIndexPage and attach BlogPages."""
        self.blog_index = BlogIndexPageFactory()

        self.blog_1 = BlogPageFactory(title="Blog 1", parent=self.blog_index)
        self.blog_2 = BlogPageFactory(title="Blog 2", parent=self.blog_index)

    def test_default_route(self):
        """This test ensures the blog index page is routable."""
        self.assertPageIsRoutable(self.blog_index)

    def test_get_context(self):
        """This test ensures the context contains the correct number of blog pages."""
        request = self.client.get(self.blog_index.url)
        context = self.blog_index.get_context(request)

        self.assertEqual(len(context["blogs"]), 2)  # It ensures both blogs exist
        self.assertEqual(context["blogs"][0].title, self.blog_2.title)
