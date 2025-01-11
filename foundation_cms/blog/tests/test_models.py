from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.blog.models import BlogIndexPage, BlogPage
from foundation_cms.profiles.models import Profile


class BlogPageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.blog_index = BlogIndexPage.objects.create(
            title="Blog Index", body="This is the blog index body."
        )
        self.profile = Profile.objects.create(title="John Doe")
        self.blog_page = BlogPage.objects.create(
            title="Sample Blog",
            body="This is a sample blog body.",
            author=self.profile,
            parent=self.blog_index,
        )

    def test_default_route(self):
        self.assertPageIsRoutable(self.blog_page)

    def test_author_name(self):
        self.assertEqual(self.blog_page.author_name(), "John Doe")

    def test_author_name_default(self):
        self.blog_page.author = None
        self.assertEqual(self.blog_page.author_name(), "Mozilla Foundation")


class BlogIndexPageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.blog_index = BlogIndexPage.objects.create(
            title="Blog Index", body="This is the blog index body."
        )
        BlogPage.objects.create(
            title="Blog 1", body="Content of Blog 1", parent=self.blog_index
        )
        BlogPage.objects.create(
            title="Blog 2", body="Content of Blog 2", parent=self.blog_index
        )

    def test_default_route(self):
        self.assertPageIsRoutable(self.blog_index)

    def test_get_context(self):
        request = self.client.get(self.blog_index.url)
        context = self.blog_index.get_context(request)
        self.assertEqual(len(context["blogs"]), 2)
        self.assertEqual(context["blogs"][0].title, "Blog 2")
