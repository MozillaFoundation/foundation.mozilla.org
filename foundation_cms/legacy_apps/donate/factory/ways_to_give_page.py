from factory import Faker
from wagtail_factories import PageFactory

from foundation_cms.legacy_apps.donate.models import DonateLandingPage
from foundation_cms.legacy_apps.utility.faker import StreamfieldProvider
from foundation_cms.legacy_apps.utility.faker.helpers import reseed
from foundation_cms.legacy_apps.wagtailpages.models import OpportunityPage

Faker.add_provider(StreamfieldProvider)

streamfield_fields = ["paragraph", "linkbutton", "spacer", "quote"]


class DonateWaysToGivePageFactory(PageFactory):
    class Meta:
        # Using OpportunityPage AKA "Default Page" model
        model = OpportunityPage

    title = Faker("sentence", nb_words=2)
    body = Faker("streamfield", fields=streamfield_fields)


def generate(seed):
    reseed(seed)

    print('Generating a Donate "Ways to give" page')
    donate_home_page = DonateLandingPage.objects.get(title="Donate Now")
    DonateWaysToGivePageFactory(parent=donate_home_page, title="Ways to Give", header="", slug="ways-to-give")
