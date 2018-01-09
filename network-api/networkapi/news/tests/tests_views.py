import json

from django.test import TestCase
from networkapi.news.factory import NewsFactory


class TestNewsView(TestCase):
    """
    Test news endpoints
    """

    def setUp(self):
        """
        Generate some news
        """

        # Generate two default news
        self.news = [NewsFactory() for i in range(2)]

        # Generate different news with specific traits
        self.news.append(NewsFactory(has_expiry=True))
        self.news.append(NewsFactory(has_expiry=True, is_featured=True))
        self.news.append(NewsFactory(has_expiry=True, unpublished=True))
        self.news.append(NewsFactory(unpublished=True))
        self.news.append(NewsFactory(expired=True))
        self.news.append(NewsFactory(video=True))
        self.news.append(NewsFactory(is_featured=True))
        self.news.append(NewsFactory(video=True, is_featured=True))

    def test_view_news(self):
        """
        Make sure news view works, and excludes the unpublished and expired news
        """

        news = self.client.get('/api/news/')
        news_json = json.loads(str(news.content, 'utf-8'))
        self.assertEqual(news.status_code, 200)
        self.assertEqual(len(news_json), 7)

    def test_view_one_news(self):
        """
        Test route to a single news
        """

        news = self.client.get('/api/news/1/')
        self.assertEqual(news.status_code, 200)
