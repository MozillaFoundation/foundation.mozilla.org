import json

from django.test import TestCase
from networkapi.highlights.factory import HighlightFactory


def setup_highlights(test):
    """
    Generate some highlights
    """

    # Generate two default hightlights
    test.highlights = [HighlightFactory() for i in range(2)]

    # Generate some highlights with specific traits
    test.highlights.append(HighlightFactory(has_expiry=True))
    test.highlights.append(HighlightFactory(has_expiry=True, unpublished=True))
    test.highlights.append(HighlightFactory(unpublished=True))
    test.highlights.append(HighlightFactory(expired=True))

    # persist the highlights
    for highlight in test.highlights:
        highlight.save()


class TestHighlightView(TestCase):
    """
    Test Highlights endpoints
    """

    def test_view_highlights(self):
        """
        Make sure highlights view works,
        and excludes the unpublished and expired highlights
        """
        setup_highlights(self)
        highlights = self.client.get('/api/highlights/')
        highlights_json = json.loads(str(highlights.content, 'utf-8'))
        self.assertEqual(highlights.status_code, 200)
        self.assertEqual(len(highlights_json), 3)

    def test_view_highlight(self):
        """
        Make sure single highlight route works
        """
        setup_highlights(self)
        highlight = self.client.get('/api/highlights/1/')
        self.assertEqual(highlight.status_code, 200)
