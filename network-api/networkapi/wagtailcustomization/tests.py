from django.test import TestCase
from wagtail.contrib.redirects.models import Redirect


class LocalizedRedirectTests(TestCase):
    def test_plain_redirect(self):
        """
        Test that the base redirect works.
        """
        Redirect.objects.create(
            old_path='/test',
            redirect_link='http://example.com'
        )
        response = self.client.get('/test')
        print(response)
