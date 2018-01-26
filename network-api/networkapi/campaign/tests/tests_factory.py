from datetime import datetime, timezone
from django.test import TestCase

from networkapi.campaign.factory import PetitionFactory, CampaignFactory
from networkapi.campaign.models import Petition, Campaign


class TestPetitionFactory(TestCase):
    """
    Test PetitionFactory
    """

    def test_petition_creation(self):
        """
        PetitionFactory.create() should not raise an exception
        """

        PetitionFactory.create()

    def test_petition_return_value(self):
        """
        PetitionFactory.create() should return an instance of a Petition
        """

        self.assertIsInstance(PetitionFactory.create(), Petition)


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
