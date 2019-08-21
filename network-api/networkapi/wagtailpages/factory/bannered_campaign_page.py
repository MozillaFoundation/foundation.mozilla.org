from factory import (
    Trait,
    SubFactory
)
from wagtail.core.models import Page as WagtailPage

from networkapi.wagtailpages.models import BanneredCampaignPage
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)
from .petition import PetitionFactory
from .mini_site_namespace import MiniSiteNamespaceFactory
from .donation import DonationModalsFactory
from .abstract import CMSPageFactory


class BanneredCampaignPageFactory(CMSPageFactory):
    class Meta:
        model = BanneredCampaignPage

    class Params:
        no_cta = Trait(cta=None)

    cta = SubFactory(PetitionFactory)


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        campaign_namespace = WagtailPage.objects.get(title='bannered_campaign')
        print('bannered campaign namespace exists')
    except WagtailPage.DoesNotExist:
        print('Generating a bannered campaign namespace')
        campaign_namespace = MiniSiteNamespaceFactory.create(
            parent=home_page,
            title='bannered campaigns',
            live=False
        )
