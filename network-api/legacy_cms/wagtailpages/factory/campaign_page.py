from factory import SubFactory, Trait
from factory.django import DjangoModelFactory
from wagtail.models import Page as WagtailPage

from legacy_cms.utility.faker.helpers import get_homepage, reseed
from legacy_cms.wagtailpages.donation_modal import DonationModals
from legacy_cms.wagtailpages.models import (
    CampaignIndexPage,
    CampaignPage,
    FeaturedCampaignPageRelation,
)

from .abstract import CMSPageFactory
from .donation import DonationModalsFactory
from .index_page import IndexPageFactory
from .petition import PetitionFactory


class CampaignIndexPageFactory(IndexPageFactory):

    page_size = CampaignIndexPage.PAGE_SIZES[1][0]

    class Meta:
        model = CampaignIndexPage


class CampaignPageFactory(CMSPageFactory):
    class Meta:
        model = CampaignPage

    class Params:
        no_cta = Trait(cta=None)
        cta_show_all_fields = Trait(
            cta=SubFactory(
                PetitionFactory,
                show_country_field=True,
                show_postal_code_field=True,
                show_comment_field=True,
                share_facebook="sp_111111",  # a fake ShareProgress ID for testing
                share_twitter="sp_222222",  # a fake ShareProgress ID for testing
                share_email="sp_333333",  # a fake ShareProgress ID for testing
            )
        )

    cta = SubFactory(PetitionFactory)


class CampaignIndexFeaturedCampaignPageRelationFactory(DjangoModelFactory):
    class Meta:
        model = FeaturedCampaignPageRelation

    index_page = SubFactory(CampaignIndexPageFactory)
    featured_page = SubFactory(CampaignPageFactory)


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        campaign_index_page = CampaignIndexPage.objects.get(title="campaigns")
        print("campaign index page exists")
    except WagtailPage.DoesNotExist:
        print("Generating a campaign index page")
        campaign_index_page = CampaignIndexPageFactory.create(parent=home_page, title="campaigns", live=True)

    reseed(seed)

    print("Generating Campaign Pages under namespace")
    campaigns = [CampaignPageFactory.create(parent=campaign_index_page) for i in range(5)]

    reseed(seed)

    print("Generating Donation Modals for Campaign Pages")
    [DonationModalsFactory.create(page=campaign) for campaign in campaigns]

    reseed(seed)

    try:
        CampaignPage.objects.get(title="single-page")
        print("single-page CampaignPage already exists")
    except CampaignPage.DoesNotExist:
        print("Generating single-page CampaignPage")
        # Most Campaign Pages on prod use wide content layout,
        # Setting narrowed_page_content to False to make it easier to test the real use case
        CampaignPageFactory.create(
            parent=campaign_index_page,
            title="single-page",
            narrowed_page_content=False,
            donation_modals=[DonationModals.objects.first()],
            cta_show_all_fields=True,
        )

    reseed(seed)

    try:
        CampaignPage.objects.get(title="multi-page")
        print("multi-page CampaignPage already exists.")
    except CampaignPage.DoesNotExist:
        print("Generating multi-page CampaignPage")
        multi_page_campaign = CampaignPageFactory(parent=campaign_index_page, title="multi-page")
        [CampaignPageFactory(parent=multi_page_campaign) for k in range(3)]

    reseed(seed)

    print("Featuring all campaign pages on Campaign Index Page")
    for i, campaign in enumerate(CampaignPage.objects.all()):
        CampaignIndexFeaturedCampaignPageRelationFactory.create(
            index_page=campaign_index_page,
            featured_page=campaign,
            sort_order=i,
        )

    reseed(seed)
