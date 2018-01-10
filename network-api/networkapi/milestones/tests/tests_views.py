from django.test import TestCase

from networkapi.milestones.factory import MilestoneFactory


class TestMilestoneViews(TestCase):

    def test_milestone_view(self):
        """
        Create one Milestone and check that the headlines match
        """

        milestone = MilestoneFactory.create()

        response = self.client.get('/api/milestones/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['headline'], milestone.headline)

    def test_milestone_list_view(self):
        """
        Create multiple Milestones and check they are there
        """

        [MilestoneFactory.create() for i in range(4)]

        response = self.client.get('/api/milestones/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
