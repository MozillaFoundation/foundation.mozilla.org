from datetime import datetime, timezone
from django.test import TestCase

from networkapi.homepage.factory import (
    HomepageFactory,
    HomepageLeadersFactory,
    HomepageNewsFactory,
    HomepageHighlightsFactory,
)
from networkapi.homepage.models import Homepage
from networkapi.people.models import Person
from networkapi.news.models import News
from networkapi.highlights.models import Highlight


class TestHomepageFactory(TestCase):
    """
    Test HomepageFactory
    """

    def test_homepage_creation(self):
        """
        Creating a homepage with the Factory should not raise an exception
        """

        HomepageFactory()


class TestHomepageLeadersFactory(TestCase):
    """
    Test HomepageLeadersFactory
    """

    def test_homepage_leaders_creation(self):
        """
        Creating a HomepageLeader with the Factory should not raise an exception
        """

        HomepageLeadersFactory()

    def test_homepage_leaders_has_homepage(self):
        """
        HomepageLeadersFactory() should have a related Homepage model
        """

        homepage_leader = HomepageLeadersFactory()

        self.assertIsInstance(homepage_leader.homepage, Homepage)

    def test_homepage_leaders_has_person(self):
        """
        HomepageLeadersFactory() should have a related Person model
        """

        homepage_leader = HomepageLeadersFactory()

        self.assertIsInstance(homepage_leader.leader, Person)

class TestHomepageNewsFactory(TestCase):
    """
    Test HomepageNewsFactory
    """

    def test_homepage_news_creation(self):
        """
        Creating a HomepageNews instance with the
        Factory should not raise and exception
        """

        homepage_news = HomepageNewsFactory()

    def test_homepage_news_has_homepage(self):
        """
        HomepageNewsFactory() should generate an instance with
        a related Homepage model
        """

        homepage_news = HomepageNewsFactory()

        self.assertIsInstance(homepage_news.homepage, Homepage)

    def test_homepage_news_has_person(self):
        """
        HomepageNewsFactory() should have a related News model
        """

        homepage_news = HomepageNewsFactory()

        self.assertIsInstance(homepage_news.news, News)


class TestHomepageHightlightsFactory(TestCase):
    """
    Test HomepageHighlightsFactory
    """

    def test_homepage_highlights_creation(self):
        """
        Creating a HomepageHighlights instance with the
        Factory should not raise an exception
        """

        homepage_highlight = HomepageHighlightsFactory()

    def test_homepage_highlights_has_homepage(self):
        """
        HomepageHighlightsFactory() should generate an instance with
        a related Homepage model
        """

        homepage_highlight = HomepageHighlightsFactory()

        self.assertIsInstance(homepage_highlight.homepage, Homepage)

    def test_homepage_highlights_has_person(self):
        """
        HomepageHighlightsFactory() should have a related Highlight model
        """

        homepage_highlight = HomepageHighlightsFactory()

        self.assertIsInstance(homepage_highlight.highlights, Highlight)
