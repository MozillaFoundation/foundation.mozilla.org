from django.utils import translation
from wagtail import models as wagtail_models
from wagtail.test import utils as wagtail_test
from wagtail_localize import synctree

from foundation_cms.legacy_apps.mozfest.factory import MozfestHomepageFactory
from foundation_cms.legacy_apps.wagtailpages.models import Signup


class MozfestBaseTests(wagtail_test.WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls._setup_homepage()
        cls._setup_locales()
        # Mozfest migration 0002 creates a default mozfest signup
        # Delete all Signups to avoid conflicts
        Signup.objects.all().delete()

    @classmethod
    def _setup_homepage(cls):
        root = wagtail_models.Page.get_first_root_node()
        if not root:
            raise ValueError("A root page should exist. Something is off.")
        cls.mozfest_homepage = MozfestHomepageFactory(parent=root)

    @classmethod
    def _setup_locales(cls):
        cls.default_locale = wagtail_models.Locale.get_default()
        cls.fr_locale, _ = wagtail_models.Locale.objects.get_or_create(language_code="fr")
        cls.de_locale, _ = wagtail_models.Locale.objects.get_or_create(language_code="de")
        assert cls.fr_locale != cls.default_locale

    def setUp(self):
        self.activate_locale(self.default_locale)

    def synchronize_tree(self):
        synctree.synchronize_tree(source_locale=self.default_locale, target_locale=self.fr_locale)

    def activate_locale(self, locale):
        translation.activate(locale.language_code)
