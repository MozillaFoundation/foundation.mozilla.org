from os.path import abspath, dirname, join

from django.test import TestCase
from django.utils.translation.trans_real import (
    parse_accept_lang_header as django_parse_accept_lang_header,
)
from django.utils.translation.trans_real import to_language as django_to_language
from wagtail.core.models import Collection
from wagtail.images.models import Image

from networkapi.wagtailpages import (
    language_code_to_iso_3166,
    parse_accept_lang_header,
    to_language,
)
from networkapi.wagtailpages.utils import create_wagtail_image


class TestCreateWagtailImageUtility(TestCase):
    def setUp(self):
        self.image_path = abspath(join(dirname(__file__), "../../media/images/placeholders/products/teddy.jpg"))

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
