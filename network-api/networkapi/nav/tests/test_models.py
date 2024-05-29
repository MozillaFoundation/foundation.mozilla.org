import wagtail_factories
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.utils import translation
from wagtail.blocks import StreamBlockValidationError

from networkapi.nav import factories as nav_factories
from networkapi.nav import models as nav_models
from networkapi.wagtailpages.factory import blog as blog_factories
from networkapi.wagtailpages.factory import image_factory as image_factories
from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages.tests.blog.test_blog_index import BlogIndexTestCase


class NavMenuTests(TestCase):
    def test_default_factory(self):
        """Test that the default factory creates a NavMenu with 4 dropdowns."""
        menu = nav_factories.NavMenuFactory()
        self.assertIsInstance(menu, nav_models.NavMenu)
        self.assertEqual(len(menu.dropdowns), 4)

    def test_cannot_create_nav_menu_without_dropdowns(self):
        with self.assertRaises(StreamBlockValidationError):
            menu = nav_factories.NavMenuFactory(dropdowns={})
            menu.dropdowns.stream_block.clean([])

    def test_cannot_create_nav_menu_with_more_than_five_dropdowns(self):
        with self.assertRaises(StreamBlockValidationError):
            menu = nav_factories.NavMenuFactory(
                dropdowns__0="dropdown",
                dropdowns__1="dropdown",
                dropdowns__2="dropdown",
                dropdowns__3="dropdown",
                dropdowns__4="dropdown",
            )
            menu.dropdowns.stream_block.clean([])


class TestNavMenuFeaturedTopics(test_base.WagtailpagesTestCase):
    def setUp(self):
        super().setUp()
        self.menu = nav_factories.NavMenuFactory(locale=self.default_locale)
        self.login()
        self.homepage.copy_for_translation(self.fr_locale)
        self.blog_index_page = blog_factories.BlogIndexPageFactory(locale=self.default_locale, parent=self.homepage)
        self.blog_index_page.save_revision().publish()
        self.synchronize_tree()

    def test_localized_featured_topics(self) -> None:
        self.blog_index_page.slug = "blog"
        self.blog_index_page.save_revision().publish()
        # Create some topics:
        topic_a = blog_factories.BlogPageTopicFactory(locale=self.default_locale, name="Topic A")
        topic_b = blog_factories.BlogPageTopicFactory(locale=self.default_locale, name="Topic B")
        topic_c = blog_factories.BlogPageTopicFactory(locale=self.default_locale, name="Topic C")

        # Associate the topics with the menu:
        nav_factories.NavMenuFeaturedBlogTopicRelationshipFactory(
            menu=self.menu,
            topic=topic_a,
            sort_order=2,
        )
        nav_factories.NavMenuFeaturedBlogTopicRelationshipFactory(
            menu=self.menu,
            topic=topic_b,
            sort_order=1,
        )

        # Get the localised topics:
        with self.assertNumQueries(5):
            relationships = self.menu.localized_featured_blog_topics
            topics = [relationship.topic for relationship in relationships]
            icons = [relationship.icon for relationship in relationships]

        self.assertEqual(len(topics), 2)
        self.assertEqual(len(icons), 2)
        # Topics linked to the menu should be in the list:
        self.assertIn(topic_a, topics)
        self.assertIn(topic_b, topics)
        # Topics not linked to the menu should not be in the list:
        self.assertNotIn(topic_c, topics)
        # It keeps the order:
        self.assertEqual(topics[0], topic_b)
        self.assertEqual(topics[1], topic_a)
        # It adds the proper URL to the topics:
        self.assertEqual(topics[0].url, "/en/blog/topic/topic-b/")
        self.assertEqual(topics[1].url, "/en/blog/topic/topic-a/")

    def test_number_of_queries_for_localized_featured_topics(self) -> None:
        # Create some topics:
        topics = []
        for i in range(20):
            topic = blog_factories.BlogPageTopicFactory(locale=self.default_locale, name=f"Topic {i}")
            topics.append(topic)

        # Associate the topics with the menu:
        for idx, topic in enumerate(topics):
            nav_factories.NavMenuFeaturedBlogTopicRelationshipFactory(
                menu=self.menu,
                topic=topic,
                sort_order=idx,
            )

        with self.assertNumQueries(5):
            # Make sure that this property won't blow up to N+1 queries
            relationships = self.menu.localized_featured_blog_topics
            topics = [relationship.topic for relationship in relationships]
            icons = [relationship.icon for relationship in relationships]
            self.assertEqual(len(topics), 20)
            self.assertEqual(len(icons), 20)

    def test_localized_featured_topics_with_localized_topics(self) -> None:
        # Create some topics:
        topic_a = blog_factories.BlogPageTopicFactory(locale=self.default_locale, name="Topic A")
        topic_b = blog_factories.BlogPageTopicFactory(locale=self.default_locale, name="Topic B")
        topic_c = blog_factories.BlogPageTopicFactory(locale=self.default_locale, name="Topic C")

        # Associate the topics with the menu:
        nav_factories.NavMenuFeaturedBlogTopicRelationshipFactory(
            menu=self.menu,
            topic=topic_a,
            sort_order=2,
        )
        nav_factories.NavMenuFeaturedBlogTopicRelationshipFactory(
            menu=self.menu,
            topic=topic_b,
            sort_order=1,
        )

        # Translate topics:
        self.translate_snippet(topic_a, self.fr_locale)
        topic_a_fr = topic_a.get_translation(self.fr_locale)
        self.translate_snippet(topic_b, self.fr_locale)
        topic_b_fr = topic_b.get_translation(self.fr_locale)
        self.translate_snippet(topic_c, self.fr_locale)
        topic_c_fr = topic_c.get_translation(self.fr_locale)

        # Translate the menu:
        self.translate_snippet(self.menu, self.fr_locale)
        menu_fr = self.menu.get_translation(self.fr_locale)

        # Activate the French locale:
        translation.activate(self.fr_locale.language_code)

        topic_a_fr.name = "Topic A (FR)"
        topic_a_fr.save()
        topic_b_fr.name = "Topic B (FR)"
        topic_b_fr.save()
        topic_c_fr.name = "Topic C (FR)"
        topic_c_fr.save()

        # Get the localised topics:
        relationships = menu_fr.localized_featured_blog_topics
        topics = [relationship.topic for relationship in relationships]

        self.assertEqual(len(topics), 2)
        # Topics linked to the menu should be in the list:
        self.assertIn(topic_a_fr, topics)
        self.assertIn(topic_b_fr, topics)
        # Topics not linked to the menu should not be in the list:
        self.assertNotIn(topic_c_fr, topics)
        # It keeps the order:
        self.assertEqual(topics[0], topic_b_fr)
        self.assertEqual(topics[1], topic_a_fr)

    def test_localized_featured_topics_returns_default_locale(self) -> None:
        # Create some topics:
        topic_a = blog_factories.BlogPageTopicFactory(locale=self.default_locale, name="Topic A")
        topic_b = blog_factories.BlogPageTopicFactory(locale=self.default_locale, name="Topic B")
        topic_c = blog_factories.BlogPageTopicFactory(locale=self.default_locale, name="Topic C")

        menu_fr = self.translate_snippet(self.menu, self.fr_locale)
        menu_fr = self.menu.get_translation(self.fr_locale)

        # Associate the topics with the menu:
        rel_a = nav_factories.NavMenuFeaturedBlogTopicRelationshipFactory(
            menu=self.menu,
            topic=topic_a,
            sort_order=2,
        )
        rel_b = nav_factories.NavMenuFeaturedBlogTopicRelationshipFactory(
            menu=self.menu,
            topic=topic_b,
            sort_order=1,
        )

        # Translate topics a and c (but not b) and associate them with the menu:
        self.translate_snippet(topic_a, self.fr_locale)
        topic_a_fr = topic_a.get_translation(self.fr_locale)
        self.translate_snippet(topic_c, self.fr_locale)
        topic_c_fr = topic_c.get_translation(self.fr_locale)

        nav_factories.NavMenuFeaturedBlogTopicRelationshipFactory(
            menu=menu_fr,
            topic=topic_a_fr,
            sort_order=2,
            translation_key=rel_a.translation_key,
            locale=self.fr_locale,
        )
        nav_factories.NavMenuFeaturedBlogTopicRelationshipFactory(
            menu=menu_fr,
            topic=topic_b,
            sort_order=1,
            translation_key=rel_b.translation_key,
            locale=self.fr_locale,
        )

        # Activate the French locale:
        translation.activate(self.fr_locale.language_code)
        topic_a_fr.name = "Topic A (FR)"
        topic_a_fr.save()
        topic_c_fr.name = "Topic C (FR)"
        topic_c_fr.save()

        # Get the localised topics:
        menu_fr.refresh_from_db()
        relationships = menu_fr.localized_featured_blog_topics
        topics = [relationship.topic for relationship in relationships]

        self.assertEqual(len(topics), 2)
        # The translated topic a should be in the list:
        self.assertIn(topic_a_fr, topics)
        # For topic_b, since there isn't a translation available, it should fall back to
        # the default language:
        self.assertIn(topic_b, topics)
        # Topics not linked to the menu should not be in the list:
        self.assertNotIn(topic_c, topics)
        self.assertNotIn(topic_c_fr, topics)
        # It keeps the order:
        self.assertEqual(topics[0], topic_b)
        self.assertEqual(topics[1], topic_a_fr)

    def test_icon_validation_accepts_svg_files(self):
        topic = blog_factories.BlogPageTopicFactory(locale=self.default_locale)
        # Simulate uploading an SVG file
        svg_icon = image_factories.ImageFactory(file__filename="icon.svg", file__extension="svg")

        # Create the relationship instance but do not save it yet
        topic_with_svg = nav_factories.NavMenuFeaturedBlogTopicRelationshipFactory(
            menu=self.menu,
            topic=topic,
            icon=svg_icon,
        )

        # Attempt to run the clean method, which should not raise any exceptions for valid SVG files.
        try:
            topic_with_svg.clean()
        except ValidationError as e:
            self.fail(f"Clean method raised ValidationError unexpectedly: {e}")

        # Check that the icon used in the relationship is the same as the one we created
        self.assertEqual(topic_with_svg.icon, svg_icon)

    def test_featured_blog_topic_rejects_non_svg_files(self):
        topic = blog_factories.BlogPageTopicFactory(locale=self.default_locale)

        # Simulate uploading a non-SVG file
        jpg_image = image_factories.ImageFactory(file__filename="image.jpg", file__extension="jpg")
        topic_with_jpg = nav_factories.NavMenuFeaturedBlogTopicRelationshipFactory(
            menu=self.menu,
            topic=topic,
            icon=jpg_image,
        )

        with self.assertRaises(ValidationError) as context:
            topic_with_jpg.clean()

        # Check that there's only one validation error and it's for the icon
        self.assertEqual(len(context.exception.error_dict), 1)
        self.assertTrue("icon" in context.exception.error_dict)


@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
class TestNavMenuFeaturedPosts(BlogIndexTestCase):
    def setUp(self):
        super().setUp()
        self.menu = nav_factories.NavMenuFactory(locale=self.default_locale)
        self.blog_pages = blog_factories.BlogPageFactory.create_batch(5)
        for i, blog_page in enumerate(self.blog_pages):
            blog_factories.FeaturedBlogPagesFactory(
                page=self.blog_index,
                blog=blog_page,
                sort_order=i,
            )
        self.login()

    def test_localized_featured_posts(self) -> None:
        # Get the localised posts:
        with self.assertNumQueries(4):
            posts = self.menu.localized_featured_blog_posts
            self.assertEqual(len(posts), 3)

        # Posts should be the first three of the featured blog posts:
        self.assertEqual(posts[0], self.blog_pages[0])
        self.assertEqual(posts[1], self.blog_pages[1])
        self.assertEqual(posts[2], self.blog_pages[2])
        self.assertNotIn(self.blog_pages[3], posts)
        self.assertNotIn(self.blog_pages[4], posts)


class TestNavMenuPageReferencesPerDropdown(test_base.WagtailpagesTestCase):
    def test_page_references_per_dropdown_property(self) -> None:
        # Create some pages:
        # pages ax linking to the first dropdown
        page_a1 = wagtail_factories.PageFactory(parent=self.homepage, title="Page A1")
        page_a2 = wagtail_factories.PageFactory(parent=self.homepage, title="Page A2")

        # pages bx linking to the second dropdown
        page_b1 = wagtail_factories.PageFactory(parent=self.homepage, title="Page B1")
        page_b2 = wagtail_factories.PageFactory(parent=self.homepage, title="Page B2")
        page_b3 = wagtail_factories.PageFactory(parent=self.homepage, title="Page B3")

        # Page c linked to third dropdown
        page_c = wagtail_factories.PageFactory(parent=self.homepage, title="Page C")

        # Page d not linked to any dropdowns
        page_d = wagtail_factories.PageFactory(parent=self.homepage, title="Page D")

        # Create a menu with links to the pages:
        menu = nav_factories.NavMenuFactory(
            # First dropdown | First Column | First link (page A1)
            dropdowns__0__dropdown__columns__0__nav_items__0__link_to="page",
            dropdowns__0__dropdown__columns__0__nav_items__0__page=page_a1,
            # First dropdown | First Column | Second link (external)
            dropdowns__0__dropdown__columns__0__nav_items__1__external_url_link=True,
            # First dropdown | CTA Button link (page A2)
            dropdowns__0__dropdown__button__link_to="page",
            dropdowns__0__dropdown__button__page=page_a2,
            # Second dropdown | First Column | First link (page B1)
            dropdowns__1__dropdown__columns__0__nav_items__0__link_to="page",
            dropdowns__1__dropdown__columns__0__nav_items__0__page=page_b1,
            # Second dropdown | First Column | Second link (external)
            dropdowns__1__dropdown__columns__0__nav_items__1__external_url_link=True,
            # Second dropdown | Second Column | First link (page B2)
            dropdowns__1__dropdown__columns__1_nav_items__0__link_to="page",
            dropdowns__1__dropdown__columns__1__nav_items__0__page=page_b2,
            # Second dropdown | Second Column | Second link (external)
            dropdowns__1__dropdown__columns__1__nav_items__1__external_url_link=True,
            # Second dropdown | CTA Button link (page B3)
            dropdowns__1__dropdown__button__link_to="page",
            dropdowns__1__dropdown__button__page=page_b3,
            # Third dropdown | First Column | First link (page C)
            dropdowns__2__dropdown__featured_column__0__nav_items__0__link_to="page",
            dropdowns__2__dropdown__featured_column__0__nav_items__0__page=page_c,
            # Third dropdown | First Column | Second link (external)
            dropdowns__2__dropdown__featured_column__0__nav_items__1__external_url_link=True,
        )

        # Get dropdown ids:
        dropdown_1_id = menu.dropdowns.raw_data[0]["id"]
        dropdown_2_id = menu.dropdowns.raw_data[1]["id"]
        dropdown_3_id = menu.dropdowns.raw_data[2]["id"]
        # The factory will create a fourth dropdown without any page links by default
        dropdown_4_id = menu.dropdowns.raw_data[3]["id"]

        expected = {
            dropdown_1_id: {
                "page_ids": [page_a1.id, page_a2.id],
                "self_page_id": page_a2.id,
                page_a1.id: page_a1.path,
                page_a2.id: page_a2.path,
            },
            dropdown_2_id: {
                "page_ids": [page_b1.id, page_b2.id, page_b3.id],
                "self_page_id": page_b3.id,
                page_b1.id: page_b1.path,
                page_b2.id: page_b2.path,
                page_b3.id: page_b3.path,
            },
            dropdown_3_id: {
                "page_ids": [page_c.id],
                "self_page_id": None,
                page_c.id: page_c.path,
            },
            dropdown_4_id: {"page_ids": [], "self_page_id": None},
        }

        # Get the page links:
        with self.assertNumQueries(1):
            page_references = menu.page_references_per_dropdown
            self.assertDictEqual(page_references, expected)

        # Get a flat list of page ids:
        page_ids = []
        for dropdown in page_references.values():
            page_ids.extend(dropdown["page_ids"])

        self.assertIn(page_a1.id, page_ids)
        self.assertIn(page_a2.id, page_ids)
        self.assertIn(page_b1.id, page_ids)
        self.assertIn(page_b2.id, page_ids)
        self.assertIn(page_b3.id, page_ids)
        self.assertIn(page_c.id, page_ids)
        self.assertNotIn(page_d.id, page_ids)


class TestNavMenuPageReferences(test_base.WagtailpagesTestCase):
    def test_page_references_property(self) -> None:
        # Create some pages:
        page_a = wagtail_factories.PageFactory(parent=self.homepage, title="Page A")
        page_b = wagtail_factories.PageFactory(parent=page_a, title="Page B")
        page_c = wagtail_factories.PageFactory(parent=page_b, title="Page C")
        page_d = wagtail_factories.PageFactory(parent=self.homepage, title="Page D")

        # Create a menu with links to the pages:
        menu = nav_factories.NavMenuFactory(
            dropdowns__0__dropdown__columns__0__nav_items__0__link_to="page",
            dropdowns__0__dropdown__columns__0__nav_items__0__page=page_a,
            dropdowns__0__dropdown__columns__0__nav_items__1__external_url_link=True,
            dropdowns__0__dropdown__button__link_to="page",
            dropdowns__0__dropdown__button__page=page_b,
            dropdowns__1__dropdown__featured_column__0__nav_items__0__link_to="page",
            dropdowns__1__dropdown__featured_column__0__nav_items__0__page=page_c,
            dropdowns__1__dropdown__featured_column__0__nav_items__1__external_url_link=True,
        )

        expected = {
            page_a.id: page_a.path,
            page_b.id: page_b.path,
            page_c.id: page_c.path,
        }

        # Get the page links:
        with self.assertNumQueries(1):
            page_references = menu.page_references
            self.assertDictEqual(page_references, expected)

        self.assertIn(page_a.id, page_references.keys())
        self.assertIn(page_b.id, page_references.keys())
        self.assertIn(page_c.id, page_references.keys())
        self.assertNotIn(page_d.id, page_references.keys())
