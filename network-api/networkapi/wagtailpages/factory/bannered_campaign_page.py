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
from .campaign_page import CampaignPageFactory


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
        campaign_namespace = WagtailPage.objects.get(title='bannered_campaigns')
        print('bannered campaigns namespace exists')
    except WagtailPage.DoesNotExist:
        print('Generating a bannered campaigns namespace')
        campaign_namespace = MiniSiteNamespaceFactory.create(
            parent=home_page,
            title='campaigns',
            live=False
        )

    reseed(seed)

    print('Generating Campaign Pages under namespace')
    campaigns = [CampaignPageFactory.create(parent=campaign_namespace) for i in range(5)]

    reseed(seed)

    print('Generating Donation Modals for Campaign Pages')
    [DonationModalsFactory.create(page=campaign) for campaign in campaigns]

    reseed(seed)
