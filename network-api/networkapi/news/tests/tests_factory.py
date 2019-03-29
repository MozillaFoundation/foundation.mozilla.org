from datetime import datetime, timezone
from django.test import TestCase

from networkapi.news.factory import NewsFactory
from networkapi.news.models import News


class TestNewsFactory(TestCase):
    """
    Test NewsFactory constructor
    """

    def test_news_creation(self):
        """
        NewsFactory should not raise an exception
        """

        NewsFactory.create()

    def test_news_return_value(self):
        """
        NewsFactory should return an instance of News
        """

        news = NewsFactory.create()

        self.assertIsInstance(news, News)

    def test_news_unpublished_param(self):
        """
        The unpublished kwargs should set publish_after date to sometime in the future
        """

        news = NewsFactory.create(unpublished=True)

        self.assertGreater(news.publish_after, datetime.now(tz=timezone.utc))

    def test_news_has_expiry_param(self):
        """
        The has_expiry kwarg should set the expires date to sometime in the future
        """

        news = NewsFactory.create(has_expiry=True)

        self.assertGreater(news.expires, datetime.now(tz=timezone.utc))

    def test_news_expired_param(self):
        """
        The expired kwarg should set the expires date to sometime in the past
        """

        news = NewsFactory.create(expired=True)

        self.assertLess(news.expires, datetime.now(tz=timezone.utc))

    def test_news_video_param(self):
        """
        The video kwargs should set is_video to True
        """

        news = NewsFactory.create(video=True)

        self.assertEqual(news.is_video, True)
