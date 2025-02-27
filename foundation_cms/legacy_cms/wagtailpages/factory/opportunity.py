from wagtail.models import Page as WagtailPage
from wagtail_factories import PageFactory

from legacy_cms.utility.faker.helpers import get_homepage, reseed
from legacy_cms.wagtailpages.models import InitiativesPage, OpportunityPage

from .abstract import CMSPageFactory


class OpportunityPageFactory(CMSPageFactory):
    class Meta:
        model = OpportunityPage


class InitiativesPageFactory(PageFactory):
    class Meta:
        model = InitiativesPage

    title = "initiatives"


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        initiatives_page = WagtailPage.objects.get(title="initiatives")
        print("initiatives page exists")
    except WagtailPage.DoesNotExist:
        print("Generating an empty Initiatives Page")
        initiatives_page = InitiativesPageFactory.create(parent=home_page)

    reseed(seed)

    print("Generating Opportunity Pages as child pages of an Initiative Page")
    [OpportunityPageFactory.create(parent=initiatives_page) for i in range(3)]

    reseed(seed)

    try:
        OpportunityPage.objects.get(title="single-page-opportunity")
        print("single-page OpportunityPage exists")
    except OpportunityPage.DoesNotExist:
        print("Generating single-page OpportunityPage")
        OpportunityPageFactory.create(parent=initiatives_page, title="single-page-opportunity")

    reseed(seed)

    try:
        OpportunityPage.objects.get(title="multi-page-opportunity")
        print("multi-page OpportunityPage exists")
    except OpportunityPage.DoesNotExist:
        print("Generating multi-page OpportunityPage")
        multi_page_opportunity = OpportunityPageFactory(parent=initiatives_page, title="multi-page-opportunity")
        [OpportunityPageFactory(parent=multi_page_opportunity) for k in range(3)]
