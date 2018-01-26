import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from networkapi.highlights.factory import HighlightFactory
from networkapi.highlights.views import HighlightListView, HighlightView


class TestHighlightView(TestCase):
    """
    Test HighlightView class
    """

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_view_highlight(self):
        """
        Make sure single highlight view returns a 200 status code
        """

        pk = HighlightFactory().id

        request = self.factory.get('/api/highlights/{}'.format(pk))
        response = HighlightView.as_view()(request, pk=pk)

        self.assertEqual(response.status_code, 200)

    def test_view_unpublished_highlight(self):
        """
        Make sure that an unpublished highlight isn't accessible
        """

        pk = HighlightFactory(unpublished=True).id

        request = self.factory.get('/api/highlights/{}'.format(pk))
        response = HighlightView.as_view()(request, pk=pk)

        self.assertEqual(response.status_code, 404)

    def test_view_expired_highlight(self):
        """
        Make sure that an expired highlight isn't accessible
        """

        pk = HighlightFactory(expired=True)

        request = self.factory.get('/api/highlights/{}'.format(pk))
        response = HighlightView.as_view()(request, pk=pk)

        self.assertEqual(response.status_code, 404)


class TestHighlightListView(TestCase):
    """
    Test HighlightListView class
    """

    def setUp(self):
        """
        Generate some highlights
        """

        self.factory = APIRequestFactory()

        # Generate two default highlights
        self.highlights = [HighlightFactory() for i in range(2)]

        # Generate some highlights with specific traits
        self.highlights.append(HighlightFactory(has_expiry=True))
        self.highlights.append(HighlightFactory(has_expiry=True, unpublished=True))
        self.highlights.append(HighlightFactory(unpublished=True))
        self.highlights.append(HighlightFactory(expired=True))

    def test_view_highlights_list_view(self):
        """
        Make sure highlights view returns a 200 status code
        """

        request = self.factory.get('/api/highlights/')
        response = HighlightListView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_view_highlights_list_view_length(self):
        """
        Make sure highlights view returns only the three published records
        """

        request = self.factory.get('/api/highlights/')
        response = HighlightListView.as_view()(request)
        response.render()
        response_json = json.loads(str(response.content, 'utf-8'))


        self.assertEqual(len(response_json), 3)
