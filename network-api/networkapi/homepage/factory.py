import factory
from factory.django import DjangoModelFactory

from networkapi.homepage.models import Homepage, HomepageLeaders, HomepageNews, HomepageHighlights
from networkapi.highlights.factory import HighlightFactory
from networkapi.news.factory import NewsFactory


class HomepageFactory(DjangoModelFactory):
    class Meta:
        model = Homepage


class HomepageLeadersFactory(DjangoModelFactory):
    pass


class HomepageNewsFactory(DjangoModelFactory):
    news = factory.SubFactory(NewsFactory)
    homepage = factory.SubFactory(HomepageFactory)

    class Meta:
        model = HomepageNews


class HomepageHighlightsFactory(DjangoModelFactory):
    highlights = factory.SubFactory(HighlightFactory)
    homepage = factory.SubFactory(HomepageFactory)

    class Meta:
        model = HomepageHighlights
