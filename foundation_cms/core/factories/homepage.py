import json
from pathlib import Path

import factory
from wagtail_factories import PageFactory

from foundation_cms.base.utils.helpers import (
    inject_images_into_data,
    load_manifest_with_partials,
    to_streamfield_value,
)
from foundation_cms.core.models.home_page import HomePage

DATA_DIR = Path(__file__).resolve().parent / "data"
HOMEPAGE_DIR = DATA_DIR / "homepage"
IMAGE_DIR = HOMEPAGE_DIR / "images"


class HomePageFactory(PageFactory):
    class Meta:
        model = HomePage

    title = factory.Faker("sentence", nb_words=4)

    @classmethod
    def create_from_manifest(cls, parent, slug="redesign-home"):
        """
        Load homepage content from a manifest and return a published HomePage instance.
        """
        manifest_path = HOMEPAGE_DIR / "manifest.json"
        image_manifest_path = HOMEPAGE_DIR / "image_manifest.json"

        # Build a main json content file
        raw = load_manifest_with_partials(manifest_path)
        with open(image_manifest_path, "r", encoding="utf-8") as f:
            image_manifest = json.load(f)
        # Upload & inject images into the json
        raw = inject_images_into_data(raw, image_manifest, IMAGE_DIR)

        # Grab an instance of the model to work with StreamField
        model_cls = cls._meta.model
        model_instance = model_cls()

        # Build an instance of the model, using raw json data
        instance = cls.build(
            title=raw.get("title", "Redesign Homepage"),
            slug=slug,
            hero_accordion=to_streamfield_value(
                raw.get("hero_accordion", []),
                stream_block=model_instance.hero_accordion.stream_block,
            ),
            body=to_streamfield_value(
                raw.get("body", []),
                stream_block=model_instance.body.stream_block,
            ),
        )

        # Add it to the place in the tree & publish
        parent.add_child(instance=instance)
        instance.save_revision().publish()
        return instance
