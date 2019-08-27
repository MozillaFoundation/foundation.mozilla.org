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
from .signup import SignupFactory
from .mini_site_namespace import MiniSiteNamespaceFactory
from .abstract import CMSPageFactory


class BanneredCampaignPageFactory(CMSPageFactory):
    class Meta:
        model = BanneredCampaignPage

    class Params:
        no_cta = Trait(cta=None)

    cta = SubFactory(PetitionFactory)

    signup = SubFactory(SignupFactory)


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        bannered_campaign_namespace = WagtailPage.objects.get(title='campaigns')
        print('Campaigns namespace exists')
    except WagtailPage.DoesNotExist:
        print('Generating campaigns namespace')
        bannered_campaign_namespace = MiniSiteNamespaceFactory.create(
            parent=home_page,
            title='campaigns',
            live=False
        )

    reseed(seed)

    print('Generating Bannered Campaign Pages under namespace')
    BanneredCampaignPageFactory.create(
        parent=bannered_campaign_namespace,
        title="Test Bannered Campaign"
    )

    reseed(seed)
