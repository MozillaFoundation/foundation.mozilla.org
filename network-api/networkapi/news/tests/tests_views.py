import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from networkapi.news.factory import NewsFactory
from networkapi.news.views import NewsListView, NewsView


class TestNewsView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_view_one_news(self):
        """
        Make sure single news view returns a 200 status code
        """

        pk = NewsFactory.create().id

        request = self.factory.get('/api/news/{}/'.format(pk))
        response = NewsView.as_view()(request, pk=1)

        self.assertEqual(response.status_code, 200)

    def test_view_unpublished_news(self):
        """
        Make sure that an unpublished news isn't accessible
        """

        pk = NewsFactory.create(unpublished=True).id

        request = self.factory.get('/api/news/{}/'.format(pk))
        response = NewsView.as_view()(request, pk=pk)

        self.assertEqual(response.status_code, 404)

    def test_view_expired_news(self):
        """
        Make sure that an expired news isn't accessible
        """

        pk = NewsFactory.create(expired=True).id

        request = self.factory.get('/api/news/{}/'.format(pk))
        response = NewsView.as_view()(request, pk=pk)

        self.assertEqual(response.status_code, 404)


class TestNewsListView(TestCase):

    def setUp(self):
        """
        Create some news
        """

        self.factory = APIRequestFactory()

        # Generate default news
        [NewsFactory.create() for i in range(4)]

        # Generate news with different traits
        NewsFactory.create(has_expiry=True)
        NewsFactory.create(has_expiry=True, unpublished=True)
        NewsFactory.create(unpublished=True)
        NewsFactory.create(expired=True)

    def test_news_list_view(self):
        """
        Make sure list news view returns a 200 status code
        """

        request = self.factory.get('/api/news/')
        response = NewsListView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_news_list_view_length(self):
        """
        Make sure list news view returns only the 4 published news
        """

        request = self.factory.get('/api/news/')
        response = NewsListView.as_view()(request)
        response.render()
        response_json = json.loads(response.content)

        self.assertEqual(len(response_json), 5)
