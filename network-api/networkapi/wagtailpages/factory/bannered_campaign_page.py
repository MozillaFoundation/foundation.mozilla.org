from factory import (
    Faker,
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

from .tagging import add_tags


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
    title = 'Initial test Bannered Campaign with fixed title'
    post = None

    try:
        post = BanneredCampaignPage.objects.get(title=title)
    except BanneredCampaignPage.DoesNotExist:
        post = BanneredCampaignPageFactory.create(parent=bannered_campaign_namespace, title=title)

    add_tags(post)

    for i in range(6):
        title = Faker('sentence', nb_words=6, variable_nb_words=False)
        post = None

        try:
            post = BanneredCampaignPage.objects.get(title=title)
        except BanneredCampaignPage.DoesNotExist:
            post = BanneredCampaignPageFactory.create(parent=bannered_campaign_namespace, title=title)

        add_tags(post)
