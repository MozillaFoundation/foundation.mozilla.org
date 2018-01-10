from django.test import TestCase
from networkapi.news.factory import NewsFactory


class TestNewsView(TestCase):

    def test_news_view(self):
        """
        Create one Milestone and check that the headlines match
        """

        news = NewsFactory.create()

        response = self.client.get('/api/news/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['headline'], news.headline)

    def test_news_list_view(self):
        """
        Create multiple Milestones and check they are there
        """

        [NewsFactory.create() for i in range(4)]

        response = self.client.get('/api/news/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)


# TODO: Test specific traits
# NewsFactory(has_expiry=True)
# NewsFactory(has_expiry=True, is_featured=True)
# NewsFactory(has_expiry=True, unpublished=True)
# NewsFactory(unpublished=True)
# NewsFactory(expired=True)
# NewsFactory(video=True)
# NewsFactory(is_featured=True)
# NewsFactory(video=True, is_featured=True)
