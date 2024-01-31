from os.path import abspath, dirname, join

from django.test import TestCase
from django.utils import translation
from django.utils.translation.trans_real import (
    parse_accept_lang_header as django_parse_accept_lang_header,
)
from django.utils.translation.trans_real import to_language as django_to_language
from taggit import models as tag_models
from wagtail.images.models import Image
from wagtail.models import Collection, Locale

from networkapi.wagtailpages import (
    language_code_to_iso_3166,
    parse_accept_lang_header,
    to_language,
)
from networkapi.wagtailpages.factory import blog as blog_factories
from networkapi.wagtailpages.factory.blog import (
    BlogIndexPageFactory,
    BlogPageFactory,
    FeaturedBlogPagesFactory,
)
from networkapi.wagtailpages.factory.profiles import ProfileFactory
from networkapi.wagtailpages.pagemodels.blog.blog import BlogAuthors, BlogPage
from networkapi.wagtailpages.pagemodels.profiles import Profile
from networkapi.wagtailpages.tests.base import WagtailpagesTestCase
from networkapi.wagtailpages.utils import (
    create_wagtail_image,
    get_blog_authors,
    get_content_related_by_tag,
    localize_queryset,
)


class TestGetContentRelatedByTag(TestCase):
    def test_single_page_has_same_tag(self):
        # Not using the factories here because that was throwing errors due to missing images for some reason.
        # It is unclear why this was happening, but it was not the focus of this test, so we just create the
        # objects manually.
        page = BlogPage.objects.create(title="The page", path="00010002", depth=2)
        other_page = BlogPage.objects.create(title="The other page", path="00010003", depth=2)
        tag = tag_models.Tag.objects.create(name="Test tag")
        page.tags.add(tag)
        page.save()
        other_page.tags.add(tag)
        other_page.save()

        result = get_content_related_by_tag(page)

        self.assertEqual(len(result), 1)
        self.assertListEqual(result, [other_page])


class TestCreateWagtailImageUtility(TestCase):
    def setUp(self):
        self.image_path = abspath(join(dirname(__file__), "../../../media/images/placeholders/products/teddy.jpg"))

    def create_new_image(self):
        """A generic test to ensure the image is created properly."""
        new_image = create_wagtail_image(self.image_path, image_name="fake teddy.jpg", collection_name="pni products")
        # Image was created
        self.assertIsNotNone(new_image)
        # Image has a collection and is in the proper collection
        self.assertIsNotNone(new_image.collection_id)
        self.assertEqual(new_image.collection.name, "pni products")

    def test_empty_image_name_and_no_collection(self):
        new_image = create_wagtail_image(
            self.image_path,
        )
        self.assertEqual(new_image.title, "teddy.jpg")
        self.assertEqual(new_image.collection.name, "Root")

    def test_new_collection(self):
        collection_name = "brand new collection"
        new_image = create_wagtail_image(
            self.image_path,
            image_name="fake teddy.jpg",
            collection_name=collection_name,
        )
        self.assertEqual(new_image.collection.name, collection_name)

    def test_existing_collection(self):
        new_collection_name = "first collection"

        root_collection = Collection.get_first_root_node()
        new_collection = root_collection.add_child(name=new_collection_name)
        total_images_in_new_collection = Image.objects.filter(collection=new_collection).count()
        self.assertEqual(total_images_in_new_collection, 0)

        new_image = create_wagtail_image(
            self.image_path,
            image_name="fake teddy.jpg",
            collection_name=new_collection_name,
        )
        self.assertEqual(new_image.collection.name, new_collection_name)


class TestLanguageUtilities(TestCase):
    def test_get_language_code_to_iso_3166(self):
        self.assertEqual(language_code_to_iso_3166("en-gb"), "en-GB")
        self.assertEqual(language_code_to_iso_3166("en-us"), "en-US")
        self.assertEqual(language_code_to_iso_3166("fr"), "fr")

    def test_to_language(self):
        self.assertEqual(to_language("en_US"), "en-US")

    def test_parse_accept_lang_header_returns_iso_3166_language(self):
        self.assertEqual(
            parse_accept_lang_header("en-GB,en;q=0.5"),
            (("en-GB", 1.0), ("en", 0.5)),
        )


class TestDjangoTranslationUtilityOverrides(TestCase):
    """
    Test that our overrides to Django translation functions work.
    """

    def test_to_language(self):
        self.assertEqual(django_to_language("fy_NL"), "fy-NL")

    def test_parse_accept_lang_header_returns_iso_3166_language(self):
        self.assertEqual(
            django_parse_accept_lang_header("fy-NL,fy;q=0.5"),
            (("fy-NL", 1.0), ("fy", 0.5)),
        )


class TestLocalizeQueryset(WagtailpagesTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        (cls.default_locale, _) = Locale.objects.get_or_create(language_code="en")
        (cls.active_locale, _) = Locale.objects.get_or_create(language_code="fr")

    def setUp(self):
        super().setUp()
        self.user = self.login()

    def test_localize_queryset_with_items_only_in_default_locale(self):
        """Tests that the function returns a queryset with only one version of each item
        when the queryset contains items only in default locale. tags: [happy path]"""
        # Create items only in default locale
        item1 = ProfileFactory(locale=self.default_locale)
        item2 = ProfileFactory(locale=self.default_locale)

        # Override the current language to be the active locale
        translation.activate(self.default_locale.language_code)

        # Call the function
        result = localize_queryset(Profile.objects.all())

        # Assert that only one version of each item is returned
        self.assertEqual(len(result), 2)
        # Assert that both items are returned
        self.assertIn(item1, result)
        self.assertIn(item2, result)

    def test_localize_queryset_with_items_only_in_active_locale(self):
        """Tests that the function returns a queryset with only one version of each item
        when the queryset contains items only in active locale. tags: [happy path]"""
        # Create items only in default locale
        item1 = ProfileFactory(locale=self.active_locale)
        item2 = ProfileFactory(locale=self.active_locale)

        # Override the current language to be the active locale
        translation.activate(self.active_locale.language_code)

        # Call the function
        result = localize_queryset(Profile.objects.all())

        # Assert that only one version of each item is returned
        self.assertEqual(len(result), 2)
        # Assert that both items are returned
        self.assertIn(item1, result)
        self.assertIn(item2, result)

    def test_localize_queryset_with_items_in_both_default_and_active_locales(self):
        """Tests that the function returns a queryset with only one version of each item
        when the queryset contains items in both default and active locales. tags: [happy path]"""
        # Create items in both default and active locales
        default = ProfileFactory(locale=self.default_locale)
        active = ProfileFactory(locale=self.active_locale, translation_key=default.translation_key)

        # Override the current language to be the active locale
        translation.activate(self.active_locale.language_code)

        # Call the function
        result = localize_queryset(Profile.objects.all())

        # Assert that only one version of each item is returned
        self.assertEqual(len(result), 1)
        # Assert that only the item in the active locale is returned
        self.assertNotIn(default, result)
        self.assertIn(active, result)

    def test_localize_queryset_with_multiple_items_in_both_locales(self):
        """Tests that the function returns a queryset with only one version of each item
        when the queryset contains translated and not-translated items. tags: [happy path]"""
        # Create items in default locale:
        default1 = ProfileFactory(locale=self.default_locale)
        default2 = ProfileFactory(locale=self.default_locale)
        default3 = ProfileFactory(locale=self.default_locale)
        default4 = ProfileFactory(locale=self.default_locale)

        # Translate some items to active locale:
        active1 = ProfileFactory(locale=self.active_locale, translation_key=default1.translation_key)
        active2 = ProfileFactory(locale=self.active_locale, translation_key=default2.translation_key)

        # Override the current language to be the active locale
        translation.activate(self.active_locale.language_code)

        # Call the function
        result = localize_queryset(Profile.objects.all())

        # We should see 4 items in the result
        self.assertEqual(len(result), 4)
        # For items that have translation, the active locale version should be returned
        self.assertNotIn(default1, result)
        self.assertIn(active1, result)
        self.assertNotIn(default2, result)
        self.assertIn(active2, result)
        # For items that don't have translation, the default locale version should be returned
        self.assertIn(default3, result)
        self.assertIn(default4, result)

    def test_localize_queryset_include_only_translations(self):
        """Tests the `include_only_translations` parameter."""
        # Create items in default locale:
        default1 = ProfileFactory(locale=self.default_locale)
        default2 = ProfileFactory(locale=self.default_locale)
        default3 = ProfileFactory(locale=self.default_locale)
        default4 = ProfileFactory(locale=self.default_locale)

        # Translate some items to active locale:
        active1 = ProfileFactory(locale=self.active_locale, translation_key=default1.translation_key)
        active2 = ProfileFactory(locale=self.active_locale, translation_key=default2.translation_key)

        # Override the current language to be the active locale
        translation.activate(self.active_locale.language_code)

        # Call the function
        result = localize_queryset(Profile.objects.all(), include_only_translations=True)

        # We should see 2 items in the result (only the ones that have translation)
        self.assertEqual(len(result), 2)
        # Default location items should not be in the result
        self.assertNotIn(default1, result)
        self.assertNotIn(default2, result)
        self.assertNotIn(default3, result)
        self.assertNotIn(default4, result)
        # Translated items should be returned
        self.assertIn(active1, result)
        self.assertIn(active2, result)

    def test_localize_queryset_can_retrieve_translations(self):
        """Tests that when the queryset only contains the items in the default location
        but there are translations available, that those are retrieved and replace their
        originals. tags: [edge case]"""
        # Create items in default locale:
        default1 = ProfileFactory(locale=self.default_locale)
        default2 = ProfileFactory(locale=self.default_locale)
        default3 = ProfileFactory(locale=self.default_locale)
        default4 = ProfileFactory(locale=self.default_locale)

        # Translate some items to active locale:
        active1 = ProfileFactory(
            name=default1.name, locale=self.active_locale, translation_key=default1.translation_key
        )
        active2 = ProfileFactory(
            name=default2.name, locale=self.active_locale, translation_key=default2.translation_key
        )

        # Override the current language to be the active locale
        translation.activate(self.active_locale.language_code)

        # Call the function with the default location only
        result = localize_queryset(Profile.objects.all().filter(locale=self.default_locale))

        # We should see 4 items in the result
        self.assertEqual(len(result), 4)
        # For items that have translation, the active locale version should be returned
        # `localize_queryset` should have retrieved the translations from the active location
        # and replaced the originals with them
        self.assertNotIn(default1, result)
        self.assertIn(active1, result)
        self.assertNotIn(default2, result)
        self.assertIn(active2, result)
        # For items that don't have translation, the default locale version should be returned
        self.assertIn(default3, result)
        self.assertIn(default4, result)

    def test_localize_queryset_with_empty_queryset(self):
        """Tests that the function returns an empty queryset when the input queryset is empty. tags: [edge case]"""
        # Call the function with an empty queryset
        result = localize_queryset(Profile.objects.none())

        # Assert that an empty queryset is returned
        self.assertEqual(len(result), 0)

    def test_localize_queryset_preserve_ordering(self):
        """Tests that the function can keep the ordering of the queryset."""
        # Create orderable items in default locale:
        blog_index_page = BlogIndexPageFactory(locale=self.default_locale, parent=self.homepage)

        apple = BlogPageFactory(title="Apple", locale=self.default_locale, parent=blog_index_page)
        banana = BlogPageFactory(title="Banana", locale=self.default_locale, parent=blog_index_page)
        carrot = BlogPageFactory(title="Carrot", locale=self.default_locale, parent=blog_index_page)
        orange = BlogPageFactory(title="Orange", locale=self.default_locale, parent=blog_index_page)

        FeaturedBlogPagesFactory(page=blog_index_page, blog=apple, sort_order=3)
        FeaturedBlogPagesFactory(page=blog_index_page, blog=banana, sort_order=1)
        FeaturedBlogPagesFactory(page=blog_index_page, blog=orange, sort_order=2)
        FeaturedBlogPagesFactory(page=blog_index_page, blog=carrot, sort_order=4)

        # Get the featured blog pages in the default locale
        featured_blog_pages = BlogPage.objects.filter(featured_pages_relationship__page=blog_index_page).order_by(
            "featured_pages_relationship__sort_order"
        )
        self.assertCountEqual(featured_blog_pages, [banana, orange, apple, carrot])

        # Translate some items to active locale:
        self.translate_page(apple, self.active_locale)
        self.translate_page(banana, self.active_locale)

        fr_apple = apple.get_translation(self.active_locale)
        fr_apple.title = "pomme"
        fr_apple.save_revision().publish()
        fr_banana = banana.get_translation(self.active_locale)
        fr_banana.title = "banane"
        fr_banana.save_revision().publish()

        # Override the current language to be the active locale
        self.activate_locale(self.active_locale)

        # Localize the queryset preserving the order
        result = localize_queryset(featured_blog_pages, preserve_order=True)
        # Assert that only one version of each item is returned
        self.assertEqual(len(result), 4)
        # Assert that the items are ordered by the sort order of the previous queryset
        self.assertCountEqual(result, [fr_banana, orange, fr_apple, carrot])

        # Reorder the queryset by the title:
        featured_blog_pages = featured_blog_pages.order_by("title")
        self.assertCountEqual(featured_blog_pages, [apple, banana, carrot, orange])
        # Localize the queryset without preserving the order
        result = localize_queryset(featured_blog_pages, preserve_order=False)
        # Assert that only one version of each item is returned
        self.assertEqual(len(result), 4)
        # The items now will be ordered by title again, but now using the localized titles
        self.assertCountEqual(result, [fr_banana, carrot, orange, fr_apple])

    def test_localize_queryset_include_draft_translations(self):
        """Tests the `include_draft_translations` parameter."""
        # Create orderable items in default locale:
        blog_index_page = BlogIndexPageFactory(locale=self.default_locale, parent=self.homepage)
        apple = BlogPageFactory(title="Apple", locale=self.default_locale, parent=blog_index_page, live=True)
        banana = BlogPageFactory(title="Banana", locale=self.default_locale, parent=blog_index_page, live=True)
        FeaturedBlogPagesFactory(page=blog_index_page, blog=apple, sort_order=3)
        FeaturedBlogPagesFactory(page=blog_index_page, blog=banana, sort_order=1)

        # Translate some items to active locale:
        self.translate_page(apple, self.active_locale)
        self.translate_page(banana, self.active_locale)

        fr_apple = apple.get_translation(self.active_locale)
        fr_apple.title = "pomme"
        fr_apple.live = False  # Draft translation
        fr_apple.save_revision()

        fr_banana = banana.get_translation(self.active_locale)
        fr_banana.title = "banane"
        fr_banana.live = True
        fr_banana.save_revision().publish()

        # Override the current language to be the active locale
        self.activate_locale(self.active_locale)

        featured_blog_pages = BlogPage.objects.filter(featured_pages_relationship__page=blog_index_page).order_by(
            "title"
        )
        self.assertCountEqual(featured_blog_pages, [apple, banana])

        # Localize the queryset without including draft translations
        result = localize_queryset(featured_blog_pages, include_draft_translations=False)

        # Assert that only the live pages are returned
        self.assertEqual(len(result), 2)
        self.assertCountEqual(result, [apple, fr_banana])

        # Localize the queryset including draft translations
        result = localize_queryset(featured_blog_pages, include_draft_translations=True)

        # Assert that now the draft apple translation is returned
        self.assertEqual(len(result), 2)
        self.assertCountEqual(result, [fr_banana, fr_apple])


class TestGetBlogAuthors(TestCase):
    def test_get_blog_authors(self):
        author_profile = ProfileFactory()
        blog_index = blog_factories.BlogIndexPageFactory()
        blog_factories.BlogPageFactory(parent=blog_index, authors=[BlogAuthors(author=author_profile)])
        not_blog_author_profile = ProfileFactory()

        blog_author_profiles = get_blog_authors(Profile.objects.all())

        self.assertIn(author_profile, blog_author_profiles)
        self.assertNotIn(not_blog_author_profile, blog_author_profiles)
