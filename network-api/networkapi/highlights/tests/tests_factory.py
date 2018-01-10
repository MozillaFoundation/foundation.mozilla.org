from datetime import datetime, timezone
from django.test import TestCase

from networkapi.highlights.factory import HighlightFactory


class TestHighlightFactory(TestCase):
    """
    Test HighlightFactory constructor
    """

    def test_highlight_creation(self):
        """
        Creation a Highlight with HighlightFactory should not raise an
        exception
        """

        highlight = HighlightFactory()

        self.assertIsNotNone(highlight)

    def test_highlight_unpublished_param(self):
        """
        The unpublished kwargs should set publish_after date to sometime in
        the future
        """

        highlight = HighlightFactory(unpublished=True)

        self.assertGreater(
            highlight.publish_after,
            datetime.now(tz=timezone.utc)
        )

    def test_highlight_has_expiry_param(self):
        """
        The has_expiry kwargs should set the expires date to sometime in
        the future
        """

        highlight = HighlightFactory(has_expiry=True)

        self.assertGreater(highlight.expires, datetime.now(tz=timezone.utc))

    def test_highlight_expired_param(self):
        """
        The expired kwargs should set the expires date to sometime in the past
        """

        highlight = HighlightFactory(expired=True)

        self.assertLess(highlight.expires, datetime.now(tz=timezone.utc))
