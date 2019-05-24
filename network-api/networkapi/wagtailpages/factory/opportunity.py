from wagtail.core.models import Page as WagtailPage

from networkapi.wagtailpages.models import OpportunityPage
from networkapi.utility.faker.helpers import (
    get_homepage,
    reseed
)
from .abstract import CMSPageFactory
from .mini_site_namespace import MiniSiteNamespaceFactory


class OpportunityPageFactory(CMSPageFactory):
    class Meta:
        model = OpportunityPage


def generate(seed):
    reseed(seed)
    home_page = get_homepage()

    try:
        opportunity_namespace = WagtailPage.objects.get(title='opportunity')
        print('opportunity namespace exists')
    except WagtailPage.DoesNotExist:
        print('Generating an opportunity namespace')
        opportunity_namespace = MiniSiteNamespaceFactory.create(parent=home_page, title='opportunity', live=False)

    reseed(seed)

    print('Generating Opportunity Pages under namespace')
    [OpportunityPageFactory.create(parent=opportunity_namespace) for i in range(5)]

    reseed(seed)

    try:
        OpportunityPage.objects.get(title='Global Sprint')
        print('Global Sprint OpportunityPage exists')
    except OpportunityPage.DoesNotExist:
        print('Generating Global Sprint OpportunityPage')
        OpportunityPageFactory.create(parent=opportunity_namespace, title='Global Sprint')

    reseed(seed)

    try:
        OpportunityPage.objects.get(title='single-page')
        print('single-page OpportunityPage exists')
    except OpportunityPage.DoesNotExist:
        print('Generating single-page OpportunityPage')
        OpportunityPageFactory.create(parent=opportunity_namespace, title='single-page')

    reseed(seed)

    try:
        OpportunityPage.objects.get(title='multi-page')
        print('multi-page OpportunityPage exists')
    except OpportunityPage.DoesNotExist:
        print('Generating multi-page OpportunityPage')
        multi_page_opportunity = OpportunityPageFactory(parent=opportunity_namespace, title='multi-page')
        [OpportunityPageFactory(parent=multi_page_opportunity) for k in range(3)]
