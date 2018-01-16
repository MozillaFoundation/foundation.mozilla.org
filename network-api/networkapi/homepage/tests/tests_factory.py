from django.test import TestCase

from networkapi.homepage.factory import (
    HomepageFactory,
    HomepageLeadersFactory,
    HomepageNewsFactory,
    HomepageHighlightsFactory,
)
from networkapi.homepage.models import (
    Homepage,
    HomepageLeaders,
    HomepageNews,
    HomepageHighlights,
)
from networkapi.people.models import Person
from networkapi.news.models import News
from networkapi.highlights.models import Highlight


class TestHomepageFactory(TestCase):
    """
    Test HomepageFactory
    """

    def test_homepage_creation(self):
        """
        HomepageFactory.create() should not raise an exception
        """

        HomepageFactory.create()

    def test_homepage_return_value(self):
        """
        HomepageFactory.create() should return an instance of Homepage
        """

        homepage_inst = HomepageFactory.create()

        self.assertIsInstance(homepage_inst, Homepage)


class TestHomepageLeadersFactory(TestCase):
    """
    Test HomepageLeadersFactory
    """

    def test_homepage_leaders_creation(self):
        """
        HomepageLeadersFactory.create() should not raise an exception
        """

        HomepageLeadersFactory.create()

    def test_homepage_leaders_return_value(self):
        """
        HomepageLeadersFactory.create() should return an instance of HomepageLeaders
        """

        homepage_leader = HomepageLeadersFactory.create()

        self.assertIsInstance(homepage_leader, HomepageLeaders)

    def test_homepage_leaders_has_homepage(self):
        """
        HomepageLeadersFactory.create() should have a related Homepage model
        """

        homepage_leader = HomepageLeadersFactory.create()

        self.assertIsInstance(homepage_leader.homepage, Homepage)

    def test_homepage_leaders_has_person(self):
        """
        HomepageLeadersFactory.create() should have a related Person model
        """

        homepage_leader = HomepageLeadersFactory.create()

        self.assertIsInstance(homepage_leader.leader, Person)


class TestHomepageNewsFactory(TestCase):
    """
    Test HomepageNewsFactory
    """

    def test_homepage_news_creation(self):
        """
        HomepageNewsFactory.create() should not raise an exception
        """

        HomepageNewsFactory.create()

    def test_homepage_news_return_value(self):
        """
        HomepageNewsFactory.create() should not raise an exception
        """

        homepage_news = HomepageNewsFactory.create()

        self.assertIsInstance(homepage_news, HomepageNews)

    def test_homepage_news_has_homepage(self):
        """
        HomepageNewsFactory.create() should generate an instance with
        a related Homepage model
        """

        homepage_news = HomepageNewsFactory.create()

        self.assertIsInstance(homepage_news.homepage, Homepage)

    def test_homepage_news_has_person(self):
        """
        HomepageNewsFactory.create() should have a related News model
        """

        homepage_news = HomepageNewsFactory.create()

        self.assertIsInstance(homepage_news.news, News)


class TestHomepageHighlightsFactory(TestCase):
    """
    Test HomepageHighlightsFactory
    """

    def test_homepage_highlights_creation(self):
        """
        HomepageHighlightsFactory.create() should not raise an exception
        """

        HomepageHighlightsFactory.create()

    def test_homepage_highlights_return_value(self):
        """
        HomepageHighlightsFactory.create() should return an instance of HomepageHighlights
        """

        homepage_highlight = HomepageHighlightsFactory.create()

        self.assertIsInstance(homepage_highlight, HomepageHighlights)

    def test_homepage_highlights_has_homepage(self):
        """
        HomepageHighlightsFactory.create() should generate an instance with
        a related Homepage model
        """

        homepage_highlight = HomepageHighlightsFactory.create()

        self.assertIsInstance(homepage_highlight.homepage, Homepage)

    def test_homepage_highlights_has_highlight(self):
        """
        HomepageHighlightsFactory.create() should have a related Highlight model
        """

        homepage_highlight = HomepageHighlightsFactory.create()

        self.assertIsInstance(homepage_highlight.highlights, Highlight)
