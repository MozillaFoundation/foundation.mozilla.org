from factory import SubFactory
from factory.django import DjangoModelFactory
from wagtail.models import Page as WagtailPage

from foundation_cms.legacy_apps.highlights.factory import HighlightFactory
from foundation_cms.legacy_apps.utility.faker.helpers import reseed
from foundation_cms.legacy_apps.wagtailpages.models import (
    ParticipateHighlights,
    ParticipateHighlights2,
    ParticipatePage2,
)

from .participate_page import ParticipatePage2Factory


class ParticipateFeaturedFactory(DjangoModelFactory):
    class Meta:
        abstract = True

    page = SubFactory(ParticipatePage2Factory)


class ParticipatePage2FeaturedHighlightsFactory(ParticipateFeaturedFactory):
    class Meta:
        model = ParticipateHighlights

    highlight = SubFactory(HighlightFactory)


class ParticipatePage2FeaturedHighlights2Factory(ParticipateFeaturedFactory):
    class Meta:
        model = ParticipateHighlights2

    highlight = SubFactory(HighlightFactory)


def generate(seed):
    participate_page = None

    try:
        participate_page = ParticipatePage2.objects.get(title="What you can do")
    except WagtailPage.DoesNotExist:
        print(
            "Participate page must exist. Ensure that "
            + "foundation_cms.legacy_apps.wagtailpages.factory.participage_page is executing first"
        )

    reseed(seed)

    print("Generating Participate Highlights")
    if participate_page is not None:
        featured_highlights = [HighlightFactory.create() for i in range(3)]
        participate_page.featured_highlights = [
            ParticipatePage2FeaturedHighlightsFactory.build(highlight=featured_highlights[i], sort_order=i)
            for i in range(3)
        ]
        featured_highlights2 = [HighlightFactory.create() for i in range(6)]
        participate_page.featured_highlights2 = [
            ParticipatePage2FeaturedHighlights2Factory.build(highlight=featured_highlights2[i], sort_order=i)
            for i in range(6)
        ]
        participate_page.save()
