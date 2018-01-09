from datetime import datetime
from django.test import TestCase

from networkapi.utility.utc import UTC
from networkapi.homepage.factory import (
    HomepageFactory,
    HomepageLeadersFactory,
    HomepageNewsFactory,
    HomepageHighlightsFactory,
)

utc = UTC()


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
        Creating a HomepageLeader with the Factoryshould not raise an exception
        """

        HomepageLeadersFactory()

    def test_homepage_leaders_args(self):
        """
        HomepageLeadersFactory() should accept kwargs that pass
        through to the PersonFactory SubFactory
        """

        homepage_leader = HomepageLeadersFactory(
            leader__is_featured=True
        )
        self.assertEqual(
            homepage_leader.leader.featured,
            True
        )

        homepage_leader = HomepageLeadersFactory(
            leader__unpublished=True
        )
        self.assertGreater(
            homepage_leader.leader.publish_after,
            datetime.now(tz=utc)
        )

        homepage_leader = HomepageLeadersFactory(
            leader__has_expiry=True
        )
        self.assertIsNotNone(
            homepage_leader.leader.expires
        )

        homepage_leader = HomepageLeadersFactory(
            leader__expired=True
        )
        self.assertLess(
            homepage_leader.leader.expires,
            datetime.now(tz=utc)
        )

        homepage_leader = HomepageLeadersFactory(
            leader__internet_health_issues=3
        )
        self.assertEqual(
            homepage_leader.leader.internet_health_issues.count(),
            3
        )

        custom_issue_names = ('issue 1', 'issue 2', 'issue 3',)
        homepage_leader = HomepageLeadersFactory(
            leader__internet_health_issues=custom_issue_names
        )
        self.assertEqual(
            homepage_leader.leader.internet_health_issues.count(),
            3
        )
        for idx in range(3):
            self.assertEqual(
                homepage_leader.leader.internet_health_issues.all()[idx].name,
                custom_issue_names[idx]
            )


class TestHomepageNewsFactory(TestCase):
    """
    Test HomepageNewsFactory
    """

    def test_homepage_news_creation(self):
        """
        Creating a HomepageNews instance with the
        Factory should not raise and exception
        """

        pass  # TODO: implement this


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
        self.assertIsNotNone(homepage_highlight.highlights)
        self.assertIsNotNone(homepage_highlight.homepage)

    def test_homepage_highlights_args(self):
        """
        HomepageHighlightsFactory() should accept kwargs that pass
        through to the HighlightFactory SubFactory
        """

        homepage_highlight = homepage_highlight = HomepageHighlightsFactory(
            highlights__unpublished=True
        )
        self.assertGreater(
            homepage_highlight.highlights.publish_after,
            datetime.now(tz=utc)
        )

        homepage_highlight = HomepageHighlightsFactory(
            highlights__has_expiry=True
        )
        self.assertIsNotNone(
            homepage_highlight.highlights.expires
        )

        homepage_highlight = HomepageHighlightsFactory(
            highlights__expired=True
        )
        self.assertLess(
            homepage_highlight.highlights.expires,
            datetime.now(tz=utc)
        )

        title = 'A very important project'

        homepage_highlight = HomepageHighlightsFactory(
            highlights__title=title
        )
        self.assertEqual(
            homepage_highlight.highlights.title,
            title
        )
