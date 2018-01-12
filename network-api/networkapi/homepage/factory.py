from factory import DjangoModelFactory, SubFactory

from networkapi.homepage.models import (
    Homepage,
    HomepageLeaders,
    HomepageNews,
    HomepageHighlights,
)
from networkapi.highlights.factory import HighlightFactory
from networkapi.news.factory import NewsFactory
from networkapi.people.factory import PersonFactory


class HomepageFactory(DjangoModelFactory):
    class Meta:
        model = Homepage


class HomepageLeadersFactory(DjangoModelFactory):
    class Meta:
        model = HomepageLeaders

    leader = SubFactory(PersonFactory)
    homepage = SubFactory(HomepageFactory)


class HomepageNewsFactory(DjangoModelFactory):
    class Meta:
        model = HomepageNews

    news = SubFactory(NewsFactory)
    homepage = SubFactory(HomepageFactory)


class HomepageHighlightsFactory(DjangoModelFactory):
    class Meta:
        model = HomepageHighlights

    highlights = SubFactory(HighlightFactory)
    homepage = SubFactory(HomepageFactory)
