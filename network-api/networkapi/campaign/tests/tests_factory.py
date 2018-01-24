from datetime import datetime, timezone
from django.test import TestCase

from networkapi.campaign.factory import SignupFactory, CampaignFactory
from networkapi.campaign.models import Signup, Campaign


class TestSignupFactory(TestCase):
    """
    Test SignupFactory
    """

    def test_signup_creation(self):
        """
        SignupFactory.create() should not raise an exception
        """

        SignupFactory.create()

    def test_signup_return_value(self):
        """
        SignupFactory.create() should return an instance of a Signup
        """

        self.assertIsInstance(SignupFactory.create(), Signup)


class TestCampaignFactory(TestCase):
    """
    Test CampaignFactory
    """

    def test_campaign_creation(self):
        """
        CampaignFactory.create() should not raise an exception
        """

        CampaignFactory.create()

    def test_campaign_return_value(self):
        """
        CampaignFactory.create() should return an instance of Campaign
        """

        landing_page = CampaignFactory.create()

        self.assertIsInstance(landing_page, Campaign)

    def test_set_campaign_parent(self):
        """
        CampaignFactory.create() should let you set another Campaign as a parent
        """

        parent_page = CampaignFactory.create()
        has_parent = CampaignFactory(parent=parent_page)

        self.assertIsInstance(has_parent.parent, Campaign)
        self.assertEqual(has_parent.parent, parent_page)

    def test_campaign_expired(self):
        """
        CampaignFactory.create() can generate pages that have already expired
        """

        page = CampaignFactory(has_expired=True)

        self.assertLess(page.expiry_date, datetime.now(tz=timezone.utc))
