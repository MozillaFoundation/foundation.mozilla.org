from factory import Faker, SubFactory
from wagtail_factories import PageFactory

from foundation_cms.legacy_apps.donate.factory.snippets.help_page_notice import (
    HelpPageNoticeFactory,
)
from foundation_cms.legacy_apps.donate.models import DonateHelpPage, DonateLandingPage
from foundation_cms.legacy_apps.utility.faker import StreamfieldProvider
from foundation_cms.legacy_apps.utility.faker.helpers import reseed

Faker.add_provider(StreamfieldProvider)

streamfield_fields = ["paragraph", "spacer", "image", "image_text", "quote"]


class DonateHelpPageFactory(PageFactory):
    class Meta:
        model = DonateHelpPage

    title = Faker("sentence", nb_words=2)
    body = Faker("streamfield", fields=streamfield_fields)
    notice = SubFactory(HelpPageNoticeFactory)


def generate(seed):
    reseed(seed)

    print("Generating a Help page")
    home_page = DonateLandingPage.objects.get(title="Donate Now")
    DonateHelpPageFactory(parent=home_page, title="Donate Help", slug="help")
