from factory import SubFactory
from factory.django import DjangoModelFactory

from networkapi.wagtailpages.models import (
    HomepageFeaturedHighlights,
    HomepageFeaturedNews
)
from networkapi.news.factory import NewsFactory
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)
from networkapi.highlights.factory import HighlightFactory
from .homepage import WagtailHomepageFactory


class FeaturedFactory(DjangoModelFactory):
    class Meta:
        abstract = True

    page = SubFactory(WagtailHomepageFactory)


class HomepageFeaturedHighlightsFactory(FeaturedFactory):
    class Meta:
        model = HomepageFeaturedHighlights

    highlight = SubFactory(HighlightFactory)


class HomepageFeaturedNewsFactory(FeaturedFactory):
    class Meta:
        model = HomepageFeaturedNews

    news = SubFactory(NewsFactory)


def generate(seed):
    print('Generating Homepage Highlights and News')

    home_page = get_homepage()

    reseed(seed)

    featured_highlights = [HighlightFactory.create() for i in range(6)]
    featured_news = [NewsFactory.create() for i in range(6)]

    home_page.featured_highlights = [
        HomepageFeaturedHighlightsFactory.build(highlight=featured_highlights[i]) for i in range(6)
    ]
    home_page.featured_news = [
        HomepageFeaturedNewsFactory.build(news=featured_news[i]) for i in range(6)
    ]

    home_page.save()
