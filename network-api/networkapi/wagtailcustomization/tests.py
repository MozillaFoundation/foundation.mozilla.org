from django.test import TestCase, RequestFactory

from wagtail.core.models import Site
from wagtail.contrib.redirects.models import Redirect


class LocalizedRedirectTests(TestCase):

    def setUp(self):
        site = Site.objects.get(is_default_site=True)
        redirect = Redirect.objects.create(
            old_path='/test',
            site=site,
            redirect_link='/'
        )
        redirect.save();

    def test_plain_redirect(self):
        """
        Test that the base redirect works.
        """
        response = self.client.get('/test')
        print(response)

