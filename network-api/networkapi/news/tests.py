import json

from django.test import TestCase
from networkapi.news.factory import NewsFactory


def setup_news(test):
    """
    Generate some news
    """

    # Generate two default news
    test.news = [NewsFactory() for i in range(2)]

    # Generate different news with specific traits
    test.news.append(NewsFactory(has_expiry=True))
    test.news.append(NewsFactory(has_expiry=True, on_homepage=True))
    test.news.append(NewsFactory(has_expiry=True, unpublished=True))
    test.news.append(NewsFactory(unpublished=True))
    test.news.append(NewsFactory(expired=True))
    test.news.append(NewsFactory(video=True))
    test.news.append(NewsFactory(on_homepage=True))
    test.news.append(NewsFactory(video=True, on_homepage=True))

    # persist the news
    for news in test.news:
        news.save()


class TestNewsView(TestCase):
    """
    Test news endpoints
    """

    def test_view_news(self):
        """
        Make sure news view works, and excludes the unpublished and expired news
        """
        setup_news(self)
        news = self.client.get('/api/news/')
        news_json = json.loads(str(news.content, 'utf-8'))
        print(news_json)
        self.assertEqual(news.status_code, 200)
        self.assertEqual(len(news_json), 7)
