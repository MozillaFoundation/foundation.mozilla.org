from factory import Faker
from wagtail.models import Page as WagtailPage
from wagtail_factories import PageFactory

from foundation_cms.legacy_cms.utility.faker.helpers import get_homepage, reseed
from foundation_cms.legacy_cms.wagtailpages.models import DearInternetPage

from .campaign_page import CampaignIndexPageFactory


class DearInternetPageFactory(PageFactory):
    class Meta:
        model = DearInternetPage
        exclude = (
            "title_text",
            "header_text",
            "header",
        )

    title = "#DearInternet"
    intro_texts = Faker("streamfield", fields=["intro_text"] * 3)
    letters_section_heading = Faker("sentence")
    letters = Faker("streamfield", fields=["letter"] * 15)
    cta = Faker("paragraph", nb_sentences=6, variable_nb_sentences=True)
    cta_button = Faker("streamfield", fields=["dear_internet_cta_button"])


def generate(seed):
    home_page = get_homepage()

    reseed(seed)

    try:
        campaign_index_page = WagtailPage.objects.get(title="campaigns")
        print("campaign index page exists")
    except WagtailPage.DoesNotExist:
        print("Generating a campaign index page")
        campaign_index_page = CampaignIndexPageFactory.create(parent=home_page, title="campaigns", live=True)

    reseed(seed)

    title = "#DearInternet"

    try:
        DearInternetPage.objects.get(title=title)
        print("Dear Internet page exists")
    except DearInternetPage.DoesNotExist:
        print("Generating Dear Internet under campaigns namespace")
        DearInternetPageFactory.create(parent=campaign_index_page, title=title)

    reseed(seed)
