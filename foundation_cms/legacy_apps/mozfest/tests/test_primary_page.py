from foundation_cms.legacy_apps.mozfest.factory import MozfestPrimaryPageFactory
from foundation_cms.legacy_apps.mozfest.tests.base import MozfestBaseTests
from foundation_cms.legacy_apps.wagtailpages.factory.signup import SignupFactory
from foundation_cms.legacy_apps.wagtailpages.models import Signup


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

    def test_get_mozfest_footer(self):
        signup = SignupFactory(name="Mozfest", locale=self.default_locale)
        mozfest_page = MozfestPrimaryPageFactory(parent=self.mozfest_homepage)

        mozfest_footer = mozfest_page.get_mozfest_footer()

        self.assertEqual(mozfest_footer, signup)

    def test_get_mozfest_footer_in_active_locale(self):
        signup_en = SignupFactory(name="MozFest", locale=self.default_locale)
        signup_fr = SignupFactory(name="MozFest", locale=self.fr_locale)

        self.synchronize_tree()
        mozfest_homepage_fr = self.mozfest_homepage.get_translation(self.fr_locale)
        mozfest_page_fr = MozfestPrimaryPageFactory(locale=self.fr_locale, parent=mozfest_homepage_fr)

        self.activate_locale(self.fr_locale)

        mozfest_footer = mozfest_page_fr.get_mozfest_footer()

        self.assertEqual(mozfest_footer, signup_fr)
        self.assertNotEqual(mozfest_footer, signup_en)

    def test_get_mozfest_footer_defaults_to_default_locale_if_not_available(self):
        signup_de = SignupFactory(name="mozfest", locale=self.de_locale)
        signup_default = SignupFactory(name="mozfest", locale=self.default_locale)

        self.synchronize_tree()
        mozfest_homepage_fr = self.mozfest_homepage.get_translation(self.fr_locale)
        mozfest_page_fr = MozfestPrimaryPageFactory(locale=self.fr_locale, parent=mozfest_homepage_fr)

        self.activate_locale(self.fr_locale)

        mozfest_footer = mozfest_page_fr.get_mozfest_footer()

        # Since we don't have a French signup, we should get the default locale
        self.assertEqual(mozfest_footer, signup_default)
        self.assertNotEqual(mozfest_footer, signup_de)

    def test_get_mozfest_footer_raises_exception_if_not_found(self):
        SignupFactory(name="mozfest", locale=self.de_locale)

        self.synchronize_tree()
        mozfest_homepage_fr = self.mozfest_homepage.get_translation(self.fr_locale)
        mozfest_page_fr = MozfestPrimaryPageFactory(locale=self.fr_locale, parent=mozfest_homepage_fr)

        self.activate_locale(self.fr_locale)

        # Try to get the context without a default locale or active locale Signup objects
        with self.assertRaises(Signup.DoesNotExist):
            mozfest_page_fr.get_mozfest_footer()

    def test_get_mozfest_footer_raises_exception_if_multiple_are_found(self):
        SignupFactory(name="Mozfest", locale=self.default_locale)
        SignupFactory(name="mozfest", locale=self.default_locale)
        mozfest_page = MozfestPrimaryPageFactory(parent=self.mozfest_homepage)

        with self.assertRaises(Signup.MultipleObjectsReturned):
            mozfest_page.get_mozfest_footer()
