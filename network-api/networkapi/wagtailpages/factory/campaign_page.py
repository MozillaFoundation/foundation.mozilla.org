from factory import (
    Trait,
    SubFactory
)
from wagtail.core.models import Page as WagtailPage

from networkapi.wagtailpages.models import CampaignPage
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)
from .petition import PetitionFactory
from .mini_site_namespace import MiniSiteNamespaceFactory
from .donation import DonationModalsFactory
from .abstract import CMSPageFactory


class CampaignPageFactory(CMSPageFactory):
    class Meta:
        model = CampaignPage

    class Params:
        no_cta = Trait(cta=None)

    cta = SubFactory(PetitionFactory)


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        campaign_namespace = WagtailPage.objects.get(title='campaigns')
        print('campaigns namespace exists')
    except WagtailPage.DoesNotExist:
        print('Generating a campaigns namespace')
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

    try:
        CampaignPage.objects.get(title='single-page')
        print('single-page CampaignPage already exists')
    except CampaignPage.DoesNotExist:
        print('Generating single-page CampaignPage')
        CampaignPageFactory.create(parent=campaign_namespace, title='single-page')

    reseed(seed)

    try:
        CampaignPage.objects.get(title='multi-page')
        print('multi-page CampaignPage already exists.')
    except CampaignPage.DoesNotExist:
        print('Generating multi-page CampaignPage')
        multi_page_campaign = CampaignPageFactory(parent=campaign_namespace, title='multi-page')
        [CampaignPageFactory(parent=multi_page_campaign) for k in range(3)]

    reseed(seed)
