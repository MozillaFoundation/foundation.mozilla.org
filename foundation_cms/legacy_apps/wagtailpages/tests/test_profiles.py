from django import test

from foundation_cms.legacy_apps.wagtailpages.factory import profiles as profile_factories


class ProfileTest(test.TestCase):
    def test_factory(self):
        profile_factories.ProfileFactory()
        self.assertTrue(True)

    def test_auto_slug(self):
        profile = profile_factories.ProfileFactory(name="Test Profile")
        profile.refresh_from_db()
        self.assertEqual(profile.slug, f"test-profile-{profile.pk}")
