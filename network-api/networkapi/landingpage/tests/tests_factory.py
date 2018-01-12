from datetime import datetime, timezone
from django.test import TestCase

from networkapi.landingpage.factory import SignupFactory, LandingPageFactory
from networkapi.landingpage.models import Signup, LandingPage


class TestSignupFactory(TestCase):
    """
    Test SignupFactory
    """

    def test_signup_creation(self):
        """
        SignupFactory.create() should not raise an exception
        """

        SignupFactory.create()

    def test_signup_return_value(self):
        """
        SignupFactory.create() should return an instance of a Signup
        """

        self.assertIsInstance(SignupFactory.create(), Signup)


class TestLandingPageFactory(TestCase):
    """
    Test LandingPageFactory
    """

    def test_landingpage_creation(self):
        """
        LandingPageFactory.create() should not raise an exception
        """

        LandingPageFactory.create()

    def test_landingpage_return_value(self):
        """
        LandingPageFactory.create() should return an instance of LandingPage
        """

        landing_page = LandingPageFactory.create()

        self.assertIsInstance(landing_page, LandingPage)

    def test_set_landing_page_parent(self):
        """
        LandingPageFactory.create() should let you set another LandingPage as a parent
        """

        parent_page = LandingPageFactory.create()
        has_parent = LandingPageFactory(parent=parent_page)

        self.assertIsInstance(has_parent.parent, LandingPage)
        self.assertEqual(has_parent.parent, parent_page)

    def test_landingpage_expired(self):
        """
        LandingPageFactory.create() can generate pages that have already expired
        """

        page = LandingPageFactory(has_expired=True)

        self.assertLess(page.expiry_date, datetime.now(tz=timezone.utc))
