from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.profiles.factories import ProfileFactory, ProfilePageFactory
from foundation_cms.profiles.models import Profile


class ProfileTestCase(WagtailPageTestCase):
    def setUp(self):
        self.profile = ProfileFactory()

    def test_str_representation(self):
        """This test ensures Profile __str__ returns the correct name."""
        self.assertEqual(str(self.profile), self.profile.title)


class ProfilePageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.profile_page = ProfilePageFactory()

    def test_default_route(self):
        """This test ensures the profile page is routable."""
        self.assertPageIsRoutable(self.profile_page)

    def test_profile_association(self):
        """This test ensures the ProfilePage correctly associates with a Profile."""
        self.assertIsInstance(self.profile_page.profile, Profile)  # Ensure a correct type
        self.assertTrue(self.profile_page.bio)  # Ensure bio is generated
