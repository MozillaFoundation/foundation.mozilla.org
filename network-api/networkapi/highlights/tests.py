import json

from django.test import TestCase
from networkapi.highlights.factory import HighlightFactory


def setup_highlights(test):
    """
    Generate some highlights
    """

    test.highlights = [HighlightFactory() for i in range(2)]
    for highlight in test.highlights:
        highlight.save()


class TestHighlightView(TestCase):
    """
    Test Highlights endpoints
    """

    def test_view_highlights(self):
        """
        Make sure highlights view works
        """
        setup_highlights(self)
        highlights = self.client.get('/api/highlights/')
        highlights_json = json.loads(str(highlights.content, 'utf-8'))
        self.assertEqual(highlights.status_code, 200)
        self.assertEqual(len(highlights_json), 2)

    def test_view_highlight(self):
        """
        Make sure single highlight route works
        """
        setup_highlights(self)
        highlight = self.client.get('/api/highlights/1/')
        self.assertEqual(highlight.status_code, 200)
