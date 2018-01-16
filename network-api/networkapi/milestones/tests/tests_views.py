import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from networkapi.milestones.factory import MilestoneFactory
from networkapi.milestones.views import MilestoneView, MilestoneListView


class TestSingleMilestoneViews(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_milestone_view(self):
        """
        Make sure single milestone view returns a 200 status code
        """

        pk = MilestoneFactory.create().id

        request = self.factory.get('/api/milestones/{}'.format(pk))
        response = MilestoneView.as_view()(request, pk=pk)

        self.assertEqual(response.status_code, 200)


class TestMultipleMilestonesView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        # Create multiple milestones
        [MilestoneFactory.create() for i in range(4)]

    def test_milestone_list_view(self):
        """
        Make sure milestone list view returns a 200 status code
        """

        request = self.factory.get('/api/milestones')
        response = MilestoneListView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_milestone_list_view_length(self):
        """
        Make sure milestone list view return the right amount of milestones
        """

        request = self.factory.get('/api/milestones')
        response = MilestoneListView.as_view()(request)
        response.render()
        response_json = json.loads(response.content)

        self.assertEqual(len(response_json), 4)
