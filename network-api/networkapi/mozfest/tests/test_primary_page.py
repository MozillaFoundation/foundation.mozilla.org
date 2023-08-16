from networkapi.mozfest.factory import MozfestPrimaryPageFactory
from networkapi.mozfest.tests.base import MozfestBaseTests


class MozfestPrimaryPageTests(MozfestBaseTests):
    def test_can_create_mozfest_primary_page(self):
        mozfest_page = MozfestPrimaryPageFactory(parent=self.mozfest_homepage)
        self.assertTrue(mozfest_page.pk)

    def test_get_template(self):
        mozfest_page = MozfestPrimaryPageFactory(parent=self.mozfest_homepage)
        self.assertEqual(mozfest_page.get_template(request=None), "mozfest/mozfest_primary_page.html")

        mozfest_page.use_wide_template = True
        mozfest_page.save()
        mozfest_page.refresh_from_db()
        self.assertEqual(mozfest_page.get_template(request=None), "mozfest/mozfest_primary_page_wide.html")
