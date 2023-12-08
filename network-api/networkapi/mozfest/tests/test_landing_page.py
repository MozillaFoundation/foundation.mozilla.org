from networkapi.mozfest import factory as mozfest_factories
from networkapi.mozfest.tests import base as mozfest_tests


class MozfestLandingPageTests(mozfest_tests.MozfestBaseTests):
    def test_can_create_mozfest_landing_page(self):
        mozfest_landing_page = mozfest_factories.MozfestLandingPageFactory(parent=self.mozfest_homepage)
        self.assertTrue(mozfest_landing_page.pk)

    def test_get_template(self):
        mozfest_landing_page = mozfest_factories.MozfestLandingPageFactory(parent=self.mozfest_homepage)
        self.assertEqual(mozfest_landing_page.get_template(request=None), "mozfest/mozfest_landing_page.html")
