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

    def test_highlight_default_publish_date(self):
        """
        By Default, a highlight should have been published
        """

        highlight = HighlightFactory()
        now = datetime.now(tz=timezone.utc)

        self.assertLess(highlight.publish_after, now)

    def test_highlight_unpublished_param(self):
        """
        The unpublished kwargs should set publish_after date to sometime in
        the future
        """

        highlight = HighlightFactory(unpublished=True)
        now = datetime.now(tz=timezone.utc)

        self.assertGreater(highlight.publish_after, now)

    def test_highlight_default_expiry(self):
        """
        By Default, a highlight should not have an expiry date
        """

        highlight = HighlightFactory()
        now = datetime.now(tz=timezone.utc)

        self.assertLess(highlight.publish_after, now)


    def test_highlight_has_expiry_param(self):
        """
        The has_expiry kwargs should set the expires date to sometime in
        the future
        """

        highlight = HighlightFactory(has_expiry=True)
        now = datetime.now(tz=timezone.utc)

        self.assertGreater(highlight.expires, now)

    def test_highlight_expired_param(self):
        """
        The expired kwargs should set the expires date to sometime in the past
        """

        highlight = HighlightFactory(expired=True)
        now = datetime.now(tz=timezone.utc)

        self.assertLess(highlight.expires, now)
