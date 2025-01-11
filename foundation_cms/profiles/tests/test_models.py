from django.test import TestCase
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.profiles.models import Profile, ProfilePage


class ProfileTestCase(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(title="Jane Doe")

    def test_str_representation(self):
        self.assertEqual(str(self.profile), "Jane Doe")


class ProfilePageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.profile = Profile.objects.create(title="Jane Doe")
        self.profile_page = ProfilePage.objects.create(
            title="Jane Doe's Profile", bio="This is the bio.", profile=self.profile
        )

    def test_default_route(self):
        self.assertPageIsRoutable(self.profile_page)

    def test_profile_association(self):
        self.assertEqual(self.profile_page.profile, self.profile)
        self.assertEqual(self.profile_page.bio, "This is the bio.")
