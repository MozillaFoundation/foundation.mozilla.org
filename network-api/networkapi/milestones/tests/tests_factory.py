from django.test import TestCase

from networkapi.milestones.factory import MilestoneFactory
from networkapi.milestones.models import Milestone


class TestMilestoneFactory(TestCase):
    """
    Test the MilestoneFactory constructor
    """

    def test_milestone_creation(self):
        """
        MilestoneFactory should not throw when creating a Milestone model
        """

        MilestoneFactory.create()

    def test_milestone_return_value(self):
        """
        MilestoneFactory should return a Milestone instance
        """

        milestone = MilestoneFactory.create()

        self.assertIsInstance(milestone, Milestone)

    def test_post_generation(self):
        """
        MilestoneFactory should generate a photo.name attribute in the post_generation stage
        """

        milestone = MilestoneFactory.create()

        self.assertIsNotNone(milestone.photo.name)
