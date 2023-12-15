import http
from unittest import mock

import wagtail_factories
from django import test
from django.core import exceptions
from taggit import models as tag_models
from wagtail import models as wagtail_models

from networkapi.wagtailpages.factory import homepage as home_factory
from networkapi.wagtailpages.factory import blog as blog_factory
from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class TestBlogPage(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request_factory = test.RequestFactory()

        root_node = wagtail_models.Page.get_first_root_node()
        site = wagtail_models.Site.objects.get(is_default_site=True)
        cls.homepage = home_factory.WagtailHomepageFactory(parent=root_node)
        site.root_page = cls.homepage
        site.clean()
        site.save()
        cls.blog_index = blog_factory.BlogIndexPageFactory(parent=cls.homepage)
        cls.blog_page = blog_factory.BlogPageFactory(parent=cls.blog_index)

        cls.tag = tag_models.Tag.objects.create(name="test")
        cls.blog_page.tags.add(cls.tag)
        cls.blog_page.save()

    def create_directly_related_post(self):
        # The relation factory creates the related post.
        relation = blog_factory.RelatedBlogPostsFactory(page=self.blog_page, related_post__parent=self.blog_index)
        return relation.related_post

    def create_tag_related_post(self, post_to_tag=None):
        if post_to_tag is None:
            tag_related_post = blog_factory.BlogPageFactory(parent=self.blog_index)
        else:
            tag_related_post = post_to_tag
        tag_related_post.tags.add(self.tag)
        tag_related_post.save()
        return tag_related_post

    def create_get_request(self, url):
        request = self.request_factory.get(url)
        # This is typically set by the Wagtail middleware, but we don't have that when using the request factory.
        request.is_preview = False
        return request

    def test_page_loads(self):
        response = self.client.get(self.blog_page.url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    @mock.patch("networkapi.wagtailpages.pagemodels.blog.blog.BlogPage.get_missing_related_posts")
    def test_get_context_with_no_related_posts_no_tag_related_posts_not_preview(self, mock_get_missing_related_posts):
        request = self.create_get_request(self.blog_page.url)

        result = self.blog_page.get_context(request)

        self.assertListEqual(result["related_posts"], [])
        self.assertEqual(mock_get_missing_related_posts.call_count, 0)

    @mock.patch("networkapi.wagtailpages.pagemodels.blog.blog.BlogPage.get_missing_related_posts")
    def test_get_context_with_no_related_posts_no_tag_related_posts_not_preview(self, mock_get_missing_related_posts):
        request = self.create_get_request(self.blog_page.url)
        request.is_preview = True
        # We test the method specifically below to see that it will actually return an empty list when there are no
        # tag related posts.
        mock_get_missing_related_posts.return_value = []

        result = self.blog_page.get_context(request)

        self.assertListEqual(result["related_posts"], [])
        self.assertEqual(mock_get_missing_related_posts.call_count, 1)

    def test_get_context_when_index_page_is_live(self):
        self.assertEqual(self.blog_index.live, True)
        request = self.create_get_request(self.blog_page.url)

        result = self.blog_page.get_context(request)

        self.assertIn("blog_index", result.keys())
        self.assertEqual(result["blog_index"], self.blog_index)
        self.assertEqual(result["blog_index"].locale.language_code, "en")

    def test_get_context_when_index_page_is_not_live(self):
        self.blog_index.live = False
        self.blog_index.save()
        request = self.create_get_request(self.blog_page.url)

        result = self.blog_page.get_context(request)

        self.assertNotIn("blog_index", result.keys())

    def test_get_missing_related_posts_no_directly_related_posts_no_tag_related_posts(self):
        self.assertEqual(self.blog_page.related_posts.count(), 0)

        result = self.blog_page.get_missing_related_posts()

        self.assertListEqual(result, [])

    def test_get_missing_related_posts_three_directly_related_posts_one_tag_related_posts(self):
        self.create_directly_related_post()
        self.create_directly_related_post()
        self.create_directly_related_post()
        self.create_tag_related_post()

        result = self.blog_page.get_missing_related_posts()

        # Because we already have 3 directly related posts, we don't get the tag related post
        self.assertListEqual(result, [])
        # The limit is defined by the BlotPage.RELATED_POSTS_MAX property
        self.assertEqual(self.blog_page.RELATED_POSTS_MAX, 3)

    def test_get_missing_related_posts_no_directly_related_posts_four_tag_related_posts(self):
        self.create_tag_related_post()
        self.create_tag_related_post()
        self.create_tag_related_post()
        self.create_tag_related_post()

        result = self.blog_page.get_missing_related_posts()

        # Because we don't have any directly related posts, we get three tag related posts.
        self.assertEqual(len(result), 3)
        # We don't get the fourth tag related post because the limit is 3.
        self.assertEqual(self.blog_page.RELATED_POSTS_MAX, 3)

    def test_get_missing_related_posts_one_directly_related_posts_three_tag_related_post(self):
        self.create_directly_related_post()
        self.create_tag_related_post()
        self.create_tag_related_post()
        self.create_tag_related_post()

        result = self.blog_page.get_missing_related_posts()

        # Because we already have 1 directly related post, we only get 2 tag related posts.
        self.assertEqual(len(result), 2)

    def test_get_missing_related_posts_same_post_is_directly_and_tag_related(self):
        related_post = self.create_directly_related_post()
        self.create_tag_related_post(post_to_tag=related_post)

        result = self.blog_page.get_missing_related_posts()

        # We don't want to see the directly related post being returned as a tag related post.
        self.assertEqual(len(result), 0)

    def test_get_missing_related_posts_limit_smaller_than_directly_related(self):
        self.blog_page.RELATED_POSTS_MAX = 1
        self.blog_page.save()
        self.create_directly_related_post()
        self.create_directly_related_post()
        self.create_tag_related_post()

        result = self.blog_page.get_missing_related_posts()

        # We have more directly related posts than the limit, so we don't get any tag related posts.
        self.assertEqual(len(result), 0)

    @mock.patch("networkapi.wagtailpages.pagemodels.blog.blog.BlogPage.get_missing_related_posts")
    def test_ensure_related_posts_calls_get_missing_related_posts(self, mock_get_missing_related_posts):
        self.assertEqual(self.blog_page.related_posts.count(), 0)

        self.blog_page.ensure_related_posts()

        self.assertEqual(mock_get_missing_related_posts.call_count, 1)

    def test_ensure_related_posts_no_directly_related_posts_no_tag_related_posts(self):
        self.assertEqual(self.blog_page.related_posts.count(), 0)

        self.blog_page.ensure_related_posts()

        self.assertEqual(self.blog_page.related_posts.count(), 0)

    def test_ensure_related_posts_one_directly_related_posts_one_tag_related_posts(self):
        self.create_directly_related_post()
        self.create_tag_related_post()
        self.assertEqual(self.blog_page.related_posts.count(), 1)

        self.blog_page.ensure_related_posts()

        self.assertEqual(self.blog_page.related_posts.count(), 2)

    @mock.patch("networkapi.wagtailpages.pagemodels.blog.blog.BlogPage.ensure_related_posts")
    def test_clean_calls_ensure_related_posts(self, mock_ensure_related_posts):
        self.blog_page.clean()

        self.assertEqual(mock_ensure_related_posts.call_count, 1)

    def test_clean_when_hero_image_and_hero_video_set(self):
        self.blog_page.hero_image = wagtail_factories.ImageFactory()
        self.blog_page.hero_video = "https://example.com/video.mp4"

        with self.assertRaises(exceptions.ValidationError):
            self.blog_page.clean()

    def test_clean_when_hero_image_but_not_hero_video_set(self):
        self.blog_page.hero_image = wagtail_factories.ImageFactory()
        self.blog_page.hero_video = ""

        result = self.blog_page.clean()

        self.assertIsNone(result)

    def test_clean_when_not_hero_image_but_hero_video_set(self):
        self.blog_page.hero_image = None
        self.blog_page.hero_video = "https://example.com/video.mp4"

        result = self.blog_page.clean()

        self.assertIsNone(result)

    def test_get_meta_description_with_search_description(self):
        self.blog_page.search_description = "test description"

        result = self.blog_page.get_meta_description()

        self.assertEqual(result, "test description")

    def test_get_meta_description_no_search_description_but_body_has_paragraph(self):
        self.blog_page.search_description = ""
        self.blog_page.body = [
            ("paragraph", "<p>This is the body content in a paragraph block.</p>"),
        ]

        result = self.blog_page.get_meta_description()

        self.assertEqual(result, "This is the body content in a paragraph block.")

    def test_get_meta_description_no_search_description_but_body_has_other_block_and_paragraph(self):
        self.blog_page.search_description = ""
        self.blog_page.body = [
            ("image_text", {"text": "Text in a different block than paragraph."}),
            ("paragraph", "<p>This is the body content in a paragraph block.</p>"),
        ]

        result = self.blog_page.get_meta_description()

        # Other body blocks until the first paragraph block are ignored.
        self.assertEqual(result, "This is the body content in a paragraph block.")

    def test_get_meta_description_no_search_description_but_long_body(self):
        self.blog_page.search_description = ""
        content = "<p>This is the body content in a paragraph block.</p><p>This is the body content in a paragraph block.</p><p>This is the body content in a paragraph block.</p><p>This is the body content in a paragraph block.</p>"  # noqa: E501
        self.blog_page.body = [
            ("paragraph", content),
        ]

        result = self.blog_page.get_meta_description()

        self.assertEqual(len(result), 153)
        expected = "This is the body content in a paragraph block. This is the body content in a paragraph block. This is the body content in a paragraph block. This is the…"  # noqa: E501
        self.assertEqual(result, expected)

    def test_get_meta_description_no_search_description_but_body_with_mutiple_paragraph_blocks(self):
        self.blog_page.search_description = ""
        self.blog_page.body = [
            ("paragraph", "<p>This is the body content in the first paragraph block.</p>"),
            ("paragraph", "<p>This is the body content in the second paragraph block.</p>"), ]

        result = self.blog_page.get_meta_description()

        # Only the first paragraph block is used.
        self.assertEqual(result, "This is the body content in the first paragraph block.")

    def test_get_meta_description_no_search_description_no_body_but_search_description_on_parent(self):
        self.blog_page.search_description = ""
        self.blog_page.body = None
        self.blog_index.search_description = "Search description on the parent."

        result = self.blog_page.get_meta_description()

        self.assertEqual(result, "Search description on the parent.")

    def test_get_meta_description_no_search_description_no_body_no_search_description_on_parent(self):
        self.blog_page.search_description = ""
        self.blog_page.body = None
        self.blog_index.search_description = ""

        result = self.blog_page.get_meta_description()

        self.assertEqual(result, foundation_metadata.FoundationMetadataPageMixin.default_description)
