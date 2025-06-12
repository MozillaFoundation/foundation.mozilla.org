import json
from pathlib import Path
import factory
from wagtail_factories import PageFactory

from foundation_cms.core.models.home_page import HomePage

DATA_DIR = Path(__file__).resolve().parent / "data"


class HomePageFactory(PageFactory):
    class Meta:
        model = HomePage

    title = factory.Faker("sentence", nb_words=4)
