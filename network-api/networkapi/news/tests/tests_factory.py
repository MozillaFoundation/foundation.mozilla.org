from datetime import datetime
from django.test import TestCase

from networkapi.news.factory import NewsFactory
from networkapi.utility.utc import UTC

utc = UTC()


class TestNewsFactory(TestCase):
    """
    Test NewsFactory constructor
    """

    def test_news_creation(self):
        """
        Creating a news with the NewsFactory should not raise an exception
        """

        news = NewsFactory()

        self.assertIsNotNone(news)

    def test_news_creation_default(self):
        """
        Verify the default values applied to a News generated with the NewsFactory
        """

        news = NewsFactory()

        self.assertIsNotNone(news.headline)
        self.assertIsNotNone(news.outlet)
        self.assertIsNotNone(news.date)
        self.assertIsNotNone(news.link)
        self.assertIsNotNone(news.excerpt)
        self.assertIsNotNone(news.author)
        self.assertIsNotNone(news.glyph)
        self.assertEqual(news.featured, False)
        self.assertLess(news.publish_after, datetime.now(tz=utc))
        self.assertIsNone(news.expires)
        self.assertEqual(news.is_video, False)
        self.assertIsNotNone(news.thumbnail)

    def test_news_is_featured_param(self):
        """
        The is_featured kwargs should set featured to True
        """

        news = NewsFactory(is_featured=True)

        self.assertEqual(news.featured, True)

    def test_news_unpublished_param(self):
        """
        The unpublished kwargs should set publish_after date to sometime in the future
        """

        news = NewsFactory(unpublished=True)

        self.assertGreater(news.publish_after, datetime.now(tz=utc))

    def test_news_has_expiry_param(self):
        """
        The has_expiry kwarg should set the expires date to sometime in the future
        """

        news = NewsFactory(has_expiry=True)

        self.assertGreater(news.expires, datetime.now(tz=utc))

    def test_news_expired_param(self):
        """
        The expired kwarg should set the expires date to sometime in the past
        """

        news = NewsFactory(expired=True)

        self.assertLess(news.expires, datetime.now(tz=utc))

    def test_news_video_param(self):
        """
        The video kwargs should set is_video to True
        """

        news = NewsFactory(video=True)

        self.assertEqual(news.is_video, True)
