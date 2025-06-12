import json
from pathlib import Path

import factory
from wagtail.models import Page

from foundation_cms.base.utils.helpers import to_streamfield_value
from foundation_cms.core.models.home_page import HomePage

DATA_DIR = Path(__file__).resolve().parent / "data"


class HomePageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HomePage

    title = factory.Faker("sentence", nb_words=4)

    @classmethod
    def create_from_json(cls, parent=None, filename="homepage_data.json"):
        """
        Load homepage JSON data and build a HomePage instance with populated streamfields.
        """
        with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
            raw = json.load(f)

        model_cls = cls._meta.model
        hero_block = model_cls().hero_accordion.stream_block
        body_block = model_cls().body.stream_block

        instance = cls.build(
            title="Redesign HomePage",
            slug="redesign-home",
            hero_accordion=to_streamfield_value(raw["hero_accordion"], stream_block=hero_block),
            body=to_streamfield_value(raw.get("body", []), stream_block=body_block),
        )

        if parent:
            parent.add_child(instance=instance)
            instance.save_revision().publish()

        return instance
