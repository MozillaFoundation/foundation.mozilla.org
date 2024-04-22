from django.test import TestCase, override_settings
from django.utils import translation
from wagtail.blocks import StreamBlockValidationError

from networkapi.nav import factories as nav_factories
from networkapi.nav import models as nav_models
from networkapi.wagtailpages.factory import blog as blog_factories
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
        with self.assertNumQueries(7):
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

        with self.assertNumQueries(7):
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
