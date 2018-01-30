import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from networkapi.people.factory import PersonFactory
from networkapi.people.views import PeopleListView, PersonView


class TestPersonView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_person_view(self):
        """
        Make sure single person view returns a 200 status code
        """

        pk = PersonFactory.create().id

        request = self.factory.get('/api/person/{}'.format(pk))
        response = PersonView.as_view()(request, pk=pk)

        self.assertEqual(response.status_code, 200)


class TestPeopleListView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        # Create multiple people
        [PersonFactory.create() for i in range(4)]

    def test_people_list_view(self):
        """
        Make sure people list view returns a 200 status code
        """

        request = self.factory.get('/api/people')
        response = PeopleListView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_people_list_view_length(self):
        """
        Make sure people list view return the right amount of peoples
        """

        request = self.factory.get('/api/people')
        response = PeopleListView.as_view()(request)
        response.render()
        response_json = json.loads(response.content.decode('utf-8'))

        self.assertEqual(len(response_json), 4)
