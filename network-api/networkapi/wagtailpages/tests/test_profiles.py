from django import test

from networkapi.wagtailpages.factory import profiles as profile_factories


class ProfileTest(test.TestCase):
    def test_factory(self):
        profile_factories.ProfileFactory()
        self.assertTrue(True)
