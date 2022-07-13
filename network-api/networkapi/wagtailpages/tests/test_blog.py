import datetime
from http import HTTPStatus
import os

from django import http, test
from django.core import management
from taggit import models as tag_models
from wagtail.core import rich_text

from networkapi.wagtailpages.factory import blog as blog_factories
from networkapi.wagtailpages.factory import profiles as profile_factories
from networkapi.wagtailpages.pagemodels.blog import blog as blog_models
from networkapi.wagtailpages.pagemodels.blog import blog_index
from networkapi.wagtailpages.pagemodels.blog import blog_topic
from networkapi.wagtailpages.tests import base as test_base


# To make sure we can control the data setup for each test, we need to deactivate the
# caching behaviout that the BlogIndexPage inherits from IndexPage.
@test.override_settings(
    CACHES = {
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}
    }
)
class BlogIndexTestCase(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.page_size = blog_index.BlogIndexPage.PAGE_SIZES[0][0]
        cls.blog_index = blog_factories.BlogIndexPageFactory(
            parent=cls.homepage,
            page_size=cls.page_size,
        )

    def fill_index_pages_with_blog_pages(
        self,
        index_pages_to_fill: int = 1,
        base_title: str = 'Thisisnotthesearchterm'
    ):
        """
        Make enough blog pages to fill given number of index pages.

        Blog pages are ordered newest to oldest.

        All pages also use the same `base_title` for their `title`. For each page,
        a number is appended to the `base_title` in order of their creation. That
        means the oldest page has a `title = base_title + " 1"`.
        """
        tz = datetime.timezone.utc
        blog_page_count = self.page_size * index_pages_to_fill
        blog_pages = []
        for index in range(0, blog_page_count):
            blog_pages.append(
                blog_factories.BlogPageFactory(
                    parent=self.blog_index,
                    title=base_title + f" {index + 1}",
                    first_published_at=(
                        datetime.datetime(2020, 1, 1, tzinfo=tz)
                        + datetime.timedelta(days=index)
                    ),
                )
            )
        blog_pages.reverse()
        return blog_pages


class TestBlogIndex(BlogIndexTestCase):
    def test_page_loads(self):
        blog_factories.BlogPageFactory(parent=self.blog_index)
        url = self.blog_index.get_url()

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_loads_emtpy(self):
        url = self.blog_index.get_url()

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_templates(self):
        blog_factories.BlogPageFactory(parent=self.blog_index)
        url = self.blog_index.get_url()

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            template_name='wagtailpages/blog_index_page.html'
        )
        self.assertTemplateUsed(
            response,
            template_name='wagtailpages/fragments/entry_cards.html'
        )
        self.assertTemplateUsed(
            response,
            template_name='wagtailpages/fragments/blog_card.html'
        )

    def test_page_with_single_entry(self):
        blog_page = blog_factories.BlogPageFactory(parent=self.blog_index)
        url = self.blog_index.get_url()

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        entries = [e.specific for e in response.context['entries']]
        self.assertIn(blog_page, entries)

    def test_page_featured_posts_not_in_entries(self):
        """The posts that are featured should not be repeated in the entries."""
        unfeatured_blog_page = blog_factories.BlogPageFactory(parent=self.blog_index)
        featured_blog_page = blog_factories.BlogPageFactory(parent=self.blog_index)
        blog_factories.FeaturedBlogPagesFactory(
            page=self.blog_index,
            blog=featured_blog_page,
        )
        url = self.blog_index.get_url()

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        entries = [e.specific for e in response.context['entries']]
        self.assertIn(unfeatured_blog_page, entries)
        self.assertNotIn(featured_blog_page, entries)


class TestBlogIndexTopic(BlogIndexTestCase):
    def test_topic_route_success(self):
        topic = blog_factories.BlogPageTopicFactory(name="Test topic")
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage(
                "entries_by_topic",
                kwargs={'topic': topic.slug},
            )
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_topic_route_non_existing_topic(self):
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage(
                "entries_by_topic",
                kwargs={'topic': 'thisisnotatopic'},
            )
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class TestBlogIndexSearch(BlogIndexTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # Using a weird search query to avoid it being generated by faker.
        cls.search_term = "Aweirdsearchquery"

    @staticmethod
    def update_index():
        # Redirect the command output to /dev/null
        with open(os.devnull, 'w') as f:
            management.call_command('update_index', verbosity=0, stdout=f)

    def test_search_route_success(self):
        url = self.blog_index.get_url() + self.blog_index.reverse_subpage("search")

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            template_name='wagtailpages/blog_index_search.html'
        )

    def test_search_route_with_query_success(self):
        blog_factories.BlogPageFactory(
            parent=self.blog_index,
            title=self.search_term,
        )
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search")
            + f'?q={ self.search_term }'
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            template_name='wagtailpages/blog_index_search.html'
        )
        self.assertTemplateUsed(
            response,
            template_name='wagtailpages/fragments/blog_card.html'
        )

    def test_search_route_featured_posts_are_in_entries(self):
        """
        Even the featured posts should be in the entries.

        On the normal blog index view, we don't want the featured blog pages to be
        included in the entries. That is because they are already shown on top.
        Since we don't show featured posts up top on the search page, we want to also
        include the featured blog posts in the list of entries.
        """
        blog_pages = self.fill_index_pages_with_blog_pages(1)
        featured_blog_page = blog_pages[0]
        blog_factories.FeaturedBlogPagesFactory(
            page=self.blog_index,
            blog=featured_blog_page,
        )
        self.assertEqual(self.blog_index.featured_pages.count(), 1)
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search")
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        entries = [e.specific for e in response.context['entries']]
        for blog_page in blog_pages:
            self.assertIn(blog_page, entries)

    def test_search_route_has_more_context_variable_false(self):
        """
        The `has_more` context variable should be `False` if too few entries.

        This variable controls if the "load more" button shows.
        """
        self.fill_index_pages_with_blog_pages(1)
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search")
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(response.context['has_more'])

    def test_search_route_has_more_context_variable_true(self):
        """
        The `has_more` context variable should be `True` if enough entries.

        This variable controls if the "load more" button shows.
        """
        self.fill_index_pages_with_blog_pages(2)
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search")
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.context['has_more'])

    def test_search_route_no_results_template(self):
        blog_factories.BlogPageFactory(
            parent=self.blog_index,
            title="This is not the search term",
        )
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search")
            + f'?q={ self.search_term }'
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            template_name='wagtailpages/blog_index_search.html'
        )
        self.assertTemplateUsed(
            response,
            template_name='wagtailpages/fragments/blog_search_no_results.html'
        )

    def test_search_route_no_query(self):
        """
        Default search page with no query shows latest x entries.

        How many pages exactly depends on the page size set on the index.
        """
        blog_pages = self.fill_index_pages_with_blog_pages(2)
        first_page_of_blog_pages = blog_pages[0:self.page_size]
        second_page_of_blog_pages = blog_pages[self.page_size:]
        url = self.blog_index.get_url() + self.blog_index.reverse_subpage("search")

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        entries = response.context['entries']
        self.assertEqual(len(entries), self.page_size)
        for blog_page in first_page_of_blog_pages:
            self.assertIn(blog_page, entries)
        for blog_page in second_page_of_blog_pages:
            self.assertNotIn(blog_page, entries)

    def test_get_search_entries_title_match(self):
        match_post = blog_factories.BlogPageFactory(
            parent=self.blog_index,
            title=self.search_term
        )
        other_post = blog_factories.BlogPageFactory(parent=self.blog_index)

        results = self.blog_index.get_search_entries(query=self.search_term)

        self.assertIn(match_post, results)
        self.assertNotIn(other_post, results)

    def test_get_search_entries_topic_match(self):
        topic = blog_topic.BlogPageTopic.objects.create(title=self.search_term)
        match_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        match_post.topics.add(topic)
        match_post.save()
        self.assertIn(topic, match_post.topics.all())
        other_post = blog_factories.BlogPageFactory(parent=self.blog_index)

        results = self.blog_index.get_search_entries(query=self.search_term)

        self.assertIn(match_post, results)
        self.assertNotIn(other_post, results)

    def test_get_search_entries_author_match(self):
        author_profile = profile_factories.ProfileFactory(name=self.search_term)
        match_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        blog_models.BlogAuthors.objects.create(page=match_post, author=author_profile)
        self.assertEqual(match_post.authors.first().author, author_profile)
        other_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        self.update_index()

        results = self.blog_index.get_search_entries(query=self.search_term)

        self.assertIn(match_post, results)
        self.assertNotIn(other_post, results)

    def test_get_search_entries_tags_match(self):
        tag = tag_models.Tag.objects.create(name=self.search_term)
        match_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        match_post.tags.add(tag)
        match_post.save()
        self.assertIn(tag, match_post.tags.all())
        other_post = blog_factories.BlogPageFactory(parent=self.blog_index)

        results = self.blog_index.get_search_entries(query=self.search_term)

        self.assertIn(match_post, results)
        self.assertNotIn(other_post, results)

    def test_get_search_entries_description_match(self):
        match_post = blog_factories.BlogPageFactory(
            parent=self.blog_index,
            search_description=f'Something including the {self.search_term}',
        )
        other_post = blog_factories.BlogPageFactory(parent=self.blog_index)

        results = self.blog_index.get_search_entries(query=self.search_term)

        self.assertIn(match_post, results)
        self.assertNotIn(other_post, results)

    def test_get_search_entries_body_match(self):
        match_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        match_post.body.append((
            'paragraph',
            rich_text.RichText(
                f'<p>Some richtext containing the { self.search_term }</p>',
            ),
        ))
        match_post.save()
        other_post = blog_factories.BlogPageFactory(parent=self.blog_index)

        results = self.blog_index.get_search_entries(query=self.search_term)

        self.assertIn(match_post, results)
        self.assertNotIn(other_post, results)

    def test_get_search_entries_ranking(self):
        """
        Test ranking of the search results.

        With Postgres database search, we only have 4 weights that can be used to
        rank search results. This means within these groups we do not have fine-grained
        control over the ranking. Therefore, it is necessary to group fields and only
        check the relative position of the groups.

        """
        # Post with match in title
        title_post = blog_factories.BlogPageFactory(
            parent=self.blog_index,
            title=self.search_term
        )
        # Post with match in topic
        topic = blog_topic.BlogPageTopic.objects.create(title=self.search_term)
        topic_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        topic_post.topics.add(topic)
        topic_post.save()
        # Post with match in author
        author_profile = profile_factories.ProfileFactory(name=self.search_term)
        author_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        blog_models.BlogAuthors.objects.create(page=author_post, author=author_profile)
        # Post with match in tag
        tag = tag_models.Tag.objects.create(name=self.search_term)
        tag_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        tag_post.tags.add(tag)
        tag_post.save()
        # Post with match in description
        description_post = blog_factories.BlogPageFactory(
            parent=self.blog_index,
            search_description=self.search_term,
        )
        # Post with match in body
        body_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        body_post.body.append((
            'paragraph',
            rich_text.RichText(self.search_term),
        ))
        body_post.save()
        # Non-matching post
        other_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        self.update_index()

        results = self.blog_index.get_search_entries(query=self.search_term)

        # All expected results are returned
        self.assertIn(title_post, results)
        self.assertIn(topic_post, results)
        self.assertIn(author_post, results)
        self.assertIn(tag_post, results)
        self.assertIn(description_post, results)
        self.assertIn(body_post, results)
        self.assertNotIn(other_post, results)

        # The expected results are in the right order
        results_list = list(results)
        title_post_index = results_list.index(title_post)
        topic_post_index = results_list.index(topic_post)
        author_post_index = results_list.index(author_post)
        tag_post_index = results_list.index(tag_post)
        description_post_index = results_list.index(description_post)
        body_post_index = results_list.index(body_post)
        self.assertLess(title_post_index, topic_post_index)
        self.assertLess(title_post_index, author_post_index)
        self.assertLess(title_post_index, tag_post_index)
        # The following assertion fails sometimes unexpectedly, but sometimes passes too.
        # I am not sure at this time what causes this inconsistent behaviour.
        # self.assertLess(topic_post_index, description_post_index)
        self.assertLess(author_post_index, description_post_index)
        self.assertLess(tag_post_index, description_post_index)
        self.assertLess(description_post_index, body_post_index)

    def test_get_search_entries_ranking_non_related(self):
        """
        Test ranking of the search results based on non-related fields.

        With Postgres database search, we only have 4 weights that can be used to
        rank search results. At the moment we only have 3 fields (that not related
        fields) that we want to rank, we can test the order of the matches directly.

        """
        # Post with match in title
        title_post = blog_factories.BlogPageFactory(
            parent=self.blog_index,
            title=self.search_term
        )
        # Post with match in description
        description_post = blog_factories.BlogPageFactory(
            parent=self.blog_index,
            search_description=self.search_term,
        )
        # Post with match in body
        body_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        body_post.body.append((
            'paragraph',
            rich_text.RichText(self.search_term),
        ))
        body_post.save()
        # Non-matching post
        other_post = blog_factories.BlogPageFactory(parent=self.blog_index)
        self.update_index()

        results = self.blog_index.get_search_entries(query=self.search_term)

        # All expected results are returned
        self.assertIn(title_post, results)
        self.assertIn(description_post, results)
        self.assertIn(body_post, results)
        self.assertNotIn(other_post, results)

        # The expected results are in the right order
        self.assertEqual(title_post, results[0])
        self.assertEqual(description_post, results[1])
        self.assertEqual(body_post, results[2])

    def test_search_entries_route_without_page_parameter(self):
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search_entries")
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_search_entries_route_non_integer_page(self):
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search_entries")
            + "?page=thisisnotaninteger"
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_search_entries_route_first_page_without_blog_pages_existing(self):
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search_entries")
            # The page numbers are 0-indexed (with page 0 being included in the initial rendering of the page).
            + "?page=0"
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_search_entries_route_second_page_without_blog_pages_existing(self):
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search_entries")
            + "?page=1"
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_search_entries_route_out_of_range_page(self):
        """
        Return 404 when requested page is out of range.

        This is similar but slightly different to the above tests where no blog pages
        exist. Here blog pages do exist, but we are requesting an entries page that
        is empty.
        """
        self.fill_index_pages_with_blog_pages(1)
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search_entries")
            # Out of range because the existing page has index 0
            + "?page=1"
        )

        response = self.client.get(path=url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_search_entries_route_loads_first_page_entries_no_query(self):
        """
        Search entries route loads first of two pages.

        In this case there is no query defined, so it just loads given page of the
        latest blog pages.
        """
        # Make more than one page of blog pages to test that pagination really works.
        blog_pages = self.fill_index_pages_with_blog_pages(2)
        first_page_of_blog_pages = blog_pages[0:self.page_size]
        second_page_of_blog_pages = blog_pages[self.page_size:]
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search_entries")
            + "?page=0"
        )

        response = self.client.get(path=url)

        self.assertIsInstance(response, http.JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Though the response is a JsonResponse, we still have access to the context used by the template loader
        # See: https://docs.djangoproject.com/en/4.0/topics/testing/tools/#django.test.Response.context
        entries = response.context['entries']
        entries_html = response.json()['entries_html']
        self.assertEqual(len(entries), self.page_size)
        for blog_page in first_page_of_blog_pages:
            self.assertIn(blog_page, entries)
            self.assertInHTML(needle=blog_page.title, haystack=entries_html)
        for blog_page in second_page_of_blog_pages:
            self.assertNotIn(blog_page, entries)
        self.assertTemplateNotUsed(response, template_name='wagtailpages/fragments/entry_cards.html')
        self.assertTemplateUsed(response, template_name='wagtailpages/fragments/blog_search_item_loop.html')
        self.assertTemplateUsed(response, template_name='wagtailpages/fragments/blog_card.html')
        self.assertTrue(response.json()['has_next'])

    def test_search_entries_route_loads_second_page_entries_no_query(self):
        """
        Search entries route loads second of two pages.

        In this case there is no query defined, so it just loads given page of the
        latest blog pages.
        """
        blog_pages = self.fill_index_pages_with_blog_pages(2)
        first_page_of_blog_pages = blog_pages[0:self.page_size]
        second_page_of_blog_pages = blog_pages[self.page_size:]
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search_entries")
            + "?page=1"
        )

        response = self.client.get(path=url)

        self.assertIsInstance(response, http.JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Though the response is a JsonResponse, we still have access to the context used by the template loader
        # See: https://docs.djangoproject.com/en/4.0/topics/testing/tools/#django.test.Response.context
        entries = response.context['entries']
        entries_html = response.json()['entries_html']
        self.assertEqual(len(entries), self.page_size)
        for blog_page in first_page_of_blog_pages:
            self.assertNotIn(blog_page, entries)
        for blog_page in second_page_of_blog_pages:
            self.assertIn(blog_page, entries)
            self.assertInHTML(needle=blog_page.title, haystack=entries_html)
        self.assertTemplateNotUsed(response, template_name='wagtailpages/fragments/entry_cards.html')
        self.assertTemplateUsed(response, template_name='wagtailpages/fragments/blog_search_item_loop.html')
        self.assertTemplateUsed(response, template_name='wagtailpages/fragments/blog_card.html')
        self.assertFalse(response.json()['has_next'])

    def test_search_entries_route_loads_first_page_entries_with_query(self):
        """Search entries route loads first of two pages of search results."""
        # Make more than one page of blog pages to test that pagination really works.
        match_blog_pages = self.fill_index_pages_with_blog_pages(2, base_title=self.search_term)
        first_page_of_matches = match_blog_pages[0:self.page_size]
        second_page_of_matches = match_blog_pages[self.page_size:]
        nonmatch_blog_pages = self.fill_index_pages_with_blog_pages(2, base_title="Othertitle")
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search_entries")
            + f"?q={ self.search_term }&page=0"
        )

        response = self.client.get(path=url)

        self.assertIsInstance(response, http.JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Though the response is a JsonResponse, we still have access to the context used by the template loader
        # See: https://docs.djangoproject.com/en/4.0/topics/testing/tools/#django.test.Response.context
        entries = response.context['entries']
        self.assertEqual(len(entries), self.page_size)
        for blog_page in first_page_of_matches:
            self.assertIn(blog_page, entries)
        for blog_page in second_page_of_matches:
            self.assertNotIn(blog_page, entries)
        for blog_page in nonmatch_blog_pages:
            self.assertNotIn(blog_page, entries)

    def test_search_entries_route_loads_second_page_entries_with_query(self):
        """Search entries route loads second of two pages of search results."""
        # Make more than one page of blog pages to test that pagination really works.
        match_blog_pages = self.fill_index_pages_with_blog_pages(2, base_title=self.search_term)
        first_page_of_matches = match_blog_pages[0:self.page_size]
        second_page_of_matches = match_blog_pages[self.page_size:]
        nonmatch_blog_pages = self.fill_index_pages_with_blog_pages(2, base_title="Othertitle")
        url = (
            self.blog_index.get_url()
            + self.blog_index.reverse_subpage("search_entries")
            + f"?q={ self.search_term }&page=1"
        )

        response = self.client.get(path=url)

        self.assertIsInstance(response, http.JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Though the response is a JsonResponse, we still have access to the context used by the template loader
        # See: https://docs.djangoproject.com/en/4.0/topics/testing/tools/#django.test.Response.context
        entries = response.context['entries']
        self.assertEqual(len(entries), self.page_size)
        for blog_page in first_page_of_matches:
            self.assertNotIn(blog_page, entries)
        for blog_page in second_page_of_matches:
            self.assertIn(blog_page, entries)
        for blog_page in nonmatch_blog_pages:
            self.assertNotIn(blog_page, entries)


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
            parent=self.blog_index, authors=[blog_models.BlogAuthors(author=self.profile_1)]
        )
        self.blog_page_2 = blog_factories.BlogPageFactory(
            parent=self.blog_index, authors=[blog_models.BlogAuthors(author=self.profile_2)]
        )

    def test_search_route_success(self):
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
        self.assertNotContains(response, self.profile_2.name)
        self.assertNotContains(response, self.profile_2.tagline)
        self.assertNotContains(response, self.profile_2.introduction)

    def test_authors_detail_non_existent_id_argument(self):
        # Test object not existing results in 404 reponse
        blog_author_url = self.blog_index.get_url() + self.blog_index.reverse_subpage(
            "blog-author-detail", args=('a-non-existent-slug',)
        )
        response = self.client.get(path=blog_author_url)
        self.assertEqual(response.status_code, 404)
