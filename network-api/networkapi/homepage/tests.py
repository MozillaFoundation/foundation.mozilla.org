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

        try:
            HomepageFactory()
        except Exception as e:
            self.fail(
                'HomepageFactory() should not raise an exception: {}'.format(e)
            )


class TestHomepageLeadersFactory(TestCase):
    """
    Test HomepageLeadersFactory
    """

    def test_homepage_leaders_creation(self):
        """
        Creating a HomepageLeader with the Factory should not raise and exception
        """

        pass # TODO: implement this
        # try:
        #     HomepageLeadersFactory()
        # except Exception as e:
        #     self.fail(
        #         'HomepageLeadersFactory() should not raise an exception: {}'.format(
        #             sys.exc_info()[0]
        #         )
        #     )



class TestHomepageNewsFactory(TestCase):
    """
    Test HomepageNewsFactory
    """

    def test_homepage_news_creation(self):
        """
        Creating a HomepageNews instance with the
        Factory should not raise and exception
        """

        pass # TODO: implement this
        # try:
        #     HomepageLeadersFactory()
        # except Exception as e:
        #     self.fail(
        #         'HomepageLeadersFactory() should not raise an exception: {}'.format(e)
        #     )


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
        through to the hightlights sub factory
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
