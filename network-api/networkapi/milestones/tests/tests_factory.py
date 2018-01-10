from django.test import TestCase

from networkapi.milestones.factory import MilestoneFactory


class TestMilestoneFactory(TestCase):
    """
    Test the MilestoneFactory constructor
    """

    def test_milestone_creation(self):

        milestone = MilestoneFactory()

        self.assertIsNotNone(milestone)
