from factory import (
    Trait,
    SubFactory
)
from wagtail.core.models import Page as WagtailPage

from networkapi.wagtailpages.models import (
    CampaignPage,
    CampaignIndexPage,
)

from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)
from .petition import PetitionFactory

from .index_page import IndexPageFactory
from .donation import DonationModalsFactory
from .abstract import CMSPageFactory


class CampaignIndexPageFactory(IndexPageFactory):
    class Meta:
        model = CampaignIndexPage


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
        campaign_index_page = WagtailPage.objects.get(title='campaigns')
        print('campaign index page exists')
    except WagtailPage.DoesNotExist:
        print('Generating a campaign index page')
        campaign_index_page = CampaignIndexPageFactory.create(
            parent=home_page,
            title='campaigns',
            live=True
        )

    reseed(seed)

    print('Generating Campaign Pages under namespace')
    campaigns = [CampaignPageFactory.create(parent=campaign_index_page) for i in range(5)]

    reseed(seed)

    print('Generating Donation Modals for Campaign Pages')
    [DonationModalsFactory.create(page=campaign) for campaign in campaigns]

    reseed(seed)

    try:
        CampaignPage.objects.get(title='single-page')
        print('single-page CampaignPage already exists')
    except CampaignPage.DoesNotExist:
        print('Generating single-page CampaignPage')
        CampaignPageFactory.create(parent=campaign_index_page, title='single-page')

    reseed(seed)

    try:
        CampaignPage.objects.get(title='multi-page')
        print('multi-page CampaignPage already exists.')
    except CampaignPage.DoesNotExist:
        print('Generating multi-page CampaignPage')
        multi_page_campaign = CampaignPageFactory(parent=campaign_index_page, title='multi-page')
        [CampaignPageFactory(parent=multi_page_campaign) for k in range(3)]

    reseed(seed)
