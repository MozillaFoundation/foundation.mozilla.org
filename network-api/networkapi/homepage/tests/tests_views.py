from datetime import datetime, timedelta, timezone

from django.test import TestCase
from unittest import expectedFailure
from rest_framework.test import APIRequestFactory
from networkapi.homepage.views import HomepageView
from networkapi.homepage.factory import (
    HomepageFactory,
    HomepageLeadersFactory,
    HomepageNewsFactory,
    HomepageHighlightsFactory,
)


class TestHomepageView(TestCase):
    """
    Test HomepageView class
    """

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_homepage_view_response_code(self):
        """
        Make sure the homepage returns a 200 status code
        """

        homepage = HomepageFactory()
        HomepageLeadersFactory(homepage=homepage)
        HomepageNewsFactory(homepage=homepage)
        HomepageHighlightsFactory(homepage=homepage)

        request = self.factory.get('/api/homepage/')
        response = HomepageView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_homepage_view_404(self):
        """
        Make sure HomepageView returns a 404 if there's no Homepage
        """

        request = self.factory.get('/api/homepage/')
        response = HomepageView.as_view()(request)

        self.assertEqual(response.status_code, 404)

    @expectedFailure
    def test_homepage_view_expired_leader(self):
        """
        Make sure an expired, featured person doesn't show up in the view

        Not sure if this should work - it seems expired Person records aren't filtered for this view
        """

        homepage = HomepageFactory()
        expire_date = datetime.now(tz=timezone.utc) - timedelta(days=1)

        HomepageLeadersFactory(
            homepage=homepage,
            leader__expires=expire_date
        )

        request = self.factory.get('/api/homepage/')
        response = HomepageView.as_view()(request)

        self.assertEqual(len(response.data['leaders']), 0)
