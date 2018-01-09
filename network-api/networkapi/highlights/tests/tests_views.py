import json

from django.test import TestCase
from networkapi.highlights.factory import HighlightFactory


class TestHighlightView(TestCase):
    """
    Test Highlights endpoints
    """

    def setUp(self):
        """
        Generate some highlights
        """

        # Generate two default hightlights
        self.highlights = [HighlightFactory() for i in range(2)]

        # Generate some highlights with specific traits
        self.highlights.append(HighlightFactory(has_expiry=True))
        self.highlights.append(HighlightFactory(has_expiry=True, unpublished=True))
        self.highlights.append(HighlightFactory(unpublished=True))
        self.highlights.append(HighlightFactory(expired=True))

    def test_view_highlights(self):
        """
        Make sure highlights view works,
        and excludes the unpublished and expired highlights
        """

        highlights = self.client.get('/api/highlights/')
        highlights_json = json.loads(str(highlights.content, 'utf-8'))
        self.assertEqual(highlights.status_code, 200)
        self.assertEqual(len(highlights_json), 3)

    def test_view_highlight(self):
        """
        Make sure single highlight route works
        """

        highlight = self.client.get('/api/highlights/1/')
        self.assertEqual(highlight.status_code, 200)
