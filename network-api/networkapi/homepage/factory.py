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
    leader = SubFactory(PersonFactory)
    homepage = SubFactory(HomepageFactory)

    class Meta:
        model = HomepageLeaders


class HomepageNewsFactory(DjangoModelFactory):
    news = SubFactory(NewsFactory)
    homepage = SubFactory(HomepageFactory)

    class Meta:
        model = HomepageNews


class HomepageHighlightsFactory(DjangoModelFactory):
    highlights = SubFactory(HighlightFactory)
    homepage = SubFactory(HomepageFactory)

    class Meta:
        model = HomepageHighlights
