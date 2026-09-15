from django.test import TestCase
from django.urls import reverse

CONFLUENCE_URL = "https://mozilla-hub.atlassian.net/wiki/spaces/FOUNDATION/pages/1824489491/How+Do+I+Wagtail"


class HowDoIWagtailRedirectTests(TestCase):
    def test_redirects_to_confluence(self):
        response = self.client.get(reverse("how-do-i-wagtail"))

        self.assertRedirects(response, CONFLUENCE_URL, fetch_redirect_response=False)
