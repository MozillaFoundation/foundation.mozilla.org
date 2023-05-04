from os.path import abspath, dirname, join

from django.test import TestCase
from django.utils import translation
from django.utils.translation.trans_real import (
    parse_accept_lang_header as django_parse_accept_lang_header,
)
from django.utils.translation.trans_real import to_language as django_to_language
from wagtail.core.models import Locale
from wagtail.images.models import Image
from wagtail.models import Collection

from networkapi.wagtailpages import (
    language_code_to_iso_3166,
    parse_accept_lang_header,
    to_language,
)
from networkapi.wagtailpages.factory import blog as blog_factories
from networkapi.wagtailpages.factory.profiles import ProfileFactory
from networkapi.wagtailpages.factory.research_hub import (
    detail_page as detail_page_factory,
)
from networkapi.wagtailpages.factory.research_hub import relations as relations_factory
from networkapi.wagtailpages.pagemodels.blog.blog import BlogAuthors
from networkapi.wagtailpages.pagemodels.profiles import Profile
from networkapi.wagtailpages.utils import (
    create_wagtail_image,
    get_blog_authors,
    get_research_authors,
    localize_queryset,
)


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


class TestLocalizeQueryset(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        (cls.default_locale, _) = Locale.objects.get_or_create(language_code="en")
        (cls.active_locale, _) = Locale.objects.get_or_create(language_code="fr")

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


class TestGetResearchAuthors(TestCase):
    def test_get_research_authors(self):
        research_author_profile = ProfileFactory()
        relations_factory.ResearchAuthorRelationFactory(
            research_detail_page=detail_page_factory.ResearchDetailPageFactory(),
            author_profile=research_author_profile,
        )
        not_research_author_profile = ProfileFactory()

        research_author_profiles = get_research_authors(Profile.objects.all())

        self.assertIn(research_author_profile, research_author_profiles)
        self.assertNotIn(not_research_author_profile, research_author_profiles)

    def test_get_research_authors_distinct(self):
        """Return research author profile only once"""

        research_author_profile = ProfileFactory()
        relations_factory.ResearchAuthorRelationFactory(
            research_detail_page=detail_page_factory.ResearchDetailPageFactory(),
            author_profile=research_author_profile,
        )
        relations_factory.ResearchAuthorRelationFactory(
            research_detail_page=detail_page_factory.ResearchDetailPageFactory(),
            author_profile=research_author_profile,
        )

        profiles = Profile.objects.all()
        profiles = get_research_authors(profiles)
        profiles = profiles.filter(id=research_author_profile.id)
        count = profiles.count()

        self.assertEqual(count, 1)


class TestGetBlogAuthors(TestCase):
    def test_get_blog_authors(self):
        author_profile = ProfileFactory()
        blog_index = blog_factories.BlogIndexPageFactory()
        blog_factories.BlogPageFactory(parent=blog_index, authors=[BlogAuthors(author=author_profile)])
        not_blog_author_profile = ProfileFactory()

        blog_author_profiles = get_blog_authors(Profile.objects.all())

        self.assertIn(author_profile, blog_author_profiles)
        self.assertNotIn(not_blog_author_profile, blog_author_profiles)
