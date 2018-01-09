from datetime import datetime
from django.test import TestCase

from networkapi.highlights.factory import HighlightFactory
from networkapi.utility.utc import UTC

utc = UTC()


class TestHighlightFactory(TestCase):
    """
    Test HighlightFactory constructor
    """

    def test_highlight_creation(self):
        """
        Creation a Highlight with HighlightFactory should not raise an exception
        """

        highlight = HighlightFactory()

        self.assertIsNotNone(highlight)

    def test_highlight_creation_default(self):
        """
        Verify the default values applied to a Highlight generated with the HighlightFactory
        """

        highlight = HighlightFactory()

        self.assertIsNotNone(highlight.title)
        self.assertIsNotNone(highlight.description)
        self.assertIsNotNone(highlight.link_label)
        self.assertIsNotNone(highlight.link_url)
        self.assertIsNotNone(highlight.image)
        self.assertIsNotNone(highlight.footer)
        self.assertLess(highlight.publish_after, datetime.now(tz=utc))
        self.assertIsNone(highlight.expires)
        self.assertEqual(highlight.order, 1)

    def test_highlight_unpublished_param(self):
        """
        The unpublished kwargs should set publish_after date to sometime in the future
        """

        highlight = HighlightFactory(unpublished=True)

        self.assertGreater(highlight.publish_after, datetime.now(tz=utc))

    def test_highlight_has_expiry_param(self):
        """
        The has_expiry kwargs should set the expires date to sometime in the future
        """

        highlight = HighlightFactory(has_expiry=True)

        self.assertGreater(highlight.expires, datetime.now(tz=utc))

    def test_highlight_expired_param(self):
        """
        The expired kwargs should set the expires date to sometime in the past
        """

        highlight = HighlightFactory(expired=True)

        self.assertLess(highlight.expires, datetime.now(tz=utc))
