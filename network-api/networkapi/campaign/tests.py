import json

from django.urls import reverse
from django.test import TestCase

from .views import crm_sqs, SQSProxy
from networkapi.wagtailpages.models import Petition, Signup

crm_sqs['client'] = SQSProxy()


class PostRouteTests(TestCase):

    def test_petition_post_route(self):
        """
        Tests the petition posting route
        """

        petition = Petition.objects.create()

        post_data = json.dumps({
            'givenNames': 'User',
            'surname': 'Tester',
            'email': 'user_test@example.org',
            'newsletterSignup': True,
            'comment': 'Test comment',
            'source': 'http://localhost/testing/petition',
            'lang': 'en',
        })

        url = reverse('petition-submission', kwargs={
            'pk': petition.id
        })

        response = self.client.post(url, post_data, content_type='application/json')
        response_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertTrue('error' in response_dict)
        self.assertEqual(response_dict['error'], 'Server is missing campaign for petition')
        print('(intentional 500 error)')

        petition.campaign_id = 123
        petition.save()

        response = self.client.post(url, post_data, content_type='application/json')
        response_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 201)

    def test_signup_post_route(self):
        """
        Tests the signup posting route
        """

        signup = Signup.objects.create()

        post_data = json.dumps({
            'email': 'user_test@example.org',
            'newsletterSignup': True,
            'source': 'http://localhost/testing/signup',
            'lang': 'en',
            'country': 'US',
        })

        url = reverse('signup-submission', kwargs={
            'pk': signup.id
        })

        response = self.client.post(url, post_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_bad_signup_post(self):
        """
        Tests the signup posting route
        """

        signup = Signup.objects.create()
        url = reverse('signup-submission', kwargs={'pk': signup.id})

        # no email

        post_data = json.dumps({
            'source': 'http://localhost/testing/signup',
        })

        response = self.client.post(url, post_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # no source

        post_data = json.dumps({
            'email': 'user_test@example.org',
        })

        response = self.client.post(url, post_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
