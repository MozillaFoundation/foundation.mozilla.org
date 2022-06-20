import datetime
from http import HTTPStatus

from networkapi.wagtailpages.factory import blog as blog_factories
from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages.factory import profiles as profile_factories
from networkapi.wagtailpages.models import Profile
from networkapi.wagtailpages.pagemodels.blog.blog import BlogAuthors


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
        entries = response.context["entries"].specific()
        self.assertIn(blog_page_7, entries)
        self.assertIn(blog_page_6, entries)
        self.assertIn(blog_page_5, entries)
        self.assertIn(blog_page_4, entries)
        self.assertIn(blog_page_3, entries)
        self.assertIn(blog_page_2, entries)
        self.assertNotIn(blog_page_1, entries)


class TestBlogIndexAuthors(test_base.WagtailpagesTestCase):
    def setUp(self):
        super().setUp()
        self.blog_index = blog_factories.BlogIndexPageFactory(parent=self.homepage)
        self.blog_index_url = self.blog_index.get_url() + self.blog_index.reverse_subpage(
            "blog_author_index"
        )

        self.profile_1 = profile_factories.ProfileFactory()
        self.profile_2 = profile_factories.ProfileFactory()
        self.profile_3 = profile_factories.ProfileFactory()

        self.blog_page_1 = blog_factories.BlogPageFactory(
            parent=self.blog_index, authors=[BlogAuthors(author=self.profile_1)]
        )
        self.blog_page_2 = blog_factories.BlogPageFactory(
            parent=self.blog_index, authors=[BlogAuthors(author=self.profile_2)]
        )

    def test_route_success(self):
        response = self.client.get(path=self.blog_index_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_authors_rendered(self):
        # Test that the blog index page renders blog authors
        response = self.client.get(path=self.blog_index_url)
        self.assertTemplateUsed(response, "wagtailpages/blog_author_index_page.html")
        self.assertContains(response, self.profile_1.name)
        self.assertContains(response, self.profile_2.name)
        self.assertNotContains(response, self.profile_3.name)
        self.assertEqual(response.render().status_code, 200)

    def test_authors_detail(self):
        blog_author_url = self.blog_index.get_url() + self.blog_index.reverse_subpage(
            "blog-author-detail", args=(self.profile_1.slug,)
        )
        response = self.client.get(path=blog_author_url)
        self.assertTemplateUsed(response, "wagtailpages/blog_author_detail_page.html")
        self.assertContains(response, self.profile_1.name)
        self.assertContains(response, self.profile_1.tagline)
        self.assertContains(response, self.profile_1.introduction)
        self.assertNotIn(self.profile_2.name, str(response.content))
        self.assertNotIn(self.profile_2.tagline, str(response.content))
        self.assertNotIn(self.profile_2.introduction, str(response.content))

    def test_authors_detail_non_existent_id_argument(self):
        # Test object not existing results in 404 reponse
        blog_author_url = self.blog_index.get_url() + self.blog_index.reverse_subpage(
            "blog-author-detail", args=('a-non-existent-slug',)
        )
        response = self.client.get(path=blog_author_url)
        self.assertEqual(response.status_code, 404)
