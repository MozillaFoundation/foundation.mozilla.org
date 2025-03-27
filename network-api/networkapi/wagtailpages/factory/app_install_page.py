from factory import Faker, SubFactory
from wagtail_factories import PageFactory

from networkapi.utility.faker.helpers import reseed
from networkapi.wagtailpages import models as pagemodels
from networkapi.wagtailpages.factory.image_factory import ImageFactory
from networkapi.wagtailpages.models import AppInstallPage

from .petition import PetitionFactory


class AppInstallPageFactory(PageFactory):
    class Meta:
        model = AppInstallPage
        exclude = (
            "title_text",
            "header_text",
            "header",
        )

    title = "Regrets Reporter Page"
    slug = "regretsreporter"
    hero_heading = Faker("text", max_nb_chars=50)
    hero_subheading = Faker("text", max_nb_chars=50)
    hero_background = SubFactory(ImageFactory)
    download_buttons = Faker("streamfield", fields=["app_install_download_button"] * 2)
    cta = SubFactory(PetitionFactory)
    body = Faker("streamfield", fields=["header", "paragraph", "image", "spacer", "image_text", "quote"])


def generate(seed):
    reseed(seed)

    print("Generating PNI Homepage")
    AppInstallPageFactory.create(
        parent=pagemodels.Homepage.objects.first(),
        title="App Install Page",
        slug="app-install-page",
    )
