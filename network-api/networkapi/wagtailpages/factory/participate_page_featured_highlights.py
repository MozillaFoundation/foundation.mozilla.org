from factory import SubFactory
from factory.django import DjangoModelFactory
from wagtail.core.models import Page as WagtailPage

from networkapi.utility.faker.helpers import reseed
from networkapi.highlights.factory import HighlightFactory
from networkapi.wagtailpages.models import (
    ParticipateHighlights,
    ParticipateHighlights2,
    ParticipatePage
)
from .participate_page import ParticipatePageFactory


class ParticipateFeaturedFactory(DjangoModelFactory):
    class Meta:
        abstract = True

    page = SubFactory(ParticipatePageFactory)


class ParticipatePageFeaturedHighlightsFactory(ParticipateFeaturedFactory):
    class Meta:
        model = ParticipateHighlights

    highlight = SubFactory(HighlightFactory)


class ParticipatePageFeaturedHighlights2Factory(ParticipateFeaturedFactory):
    class Meta:
        model = ParticipateHighlights2

    highlight = SubFactory(HighlightFactory)


def generate(seed):
    participate_page = None

    try:
        participate_page = ParticipatePage.objects.get(title='participate')
    except WagtailPage.DoesNotExist:
        print('Participate page must exist. Ensure that ' +
              'networkapi.wagtailpages.factory.participage_page is executing first')

    reseed(seed)

    print('Generating Participate Highlights')
    if participate_page is not None:
        featured_highlights = [HighlightFactory.create() for i in range(3)]
        participate_page.featured_highlights = [
            ParticipatePageFeaturedHighlightsFactory.build(highlight=featured_highlights[i]) for i in range(3)
        ]
        featured_highlights2 = [HighlightFactory.create() for i in range(6)]
        participate_page.featured_highlights2 = [
            ParticipatePageFeaturedHighlights2Factory.build(highlight=featured_highlights2[i]) for i in range(6)
        ]
        participate_page.save()
