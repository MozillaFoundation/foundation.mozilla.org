from django.urls import reverse
from django.utils import translation
from wagtail import models as wagtail_models
from wagtail.test import utils as wagtail_test
from wagtail_localize import synctree

from foundation_cms.legacy_apps.wagtailpages.factory import homepage as home_factory


class WagtailpagesTestCase(wagtail_test.WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls._setup_homepage()
        cls._setup_locales()

    @classmethod
    def _setup_homepage(cls):
        root = wagtail_models.Page.get_first_root_node()
        if not root:
            raise ValueError("A root page should exist. Something is off.")
        cls.homepage = home_factory.WagtailHomepageFactory(parent=root)

        sites = wagtail_models.Site.objects.all()
        if sites.count() != 1:
            raise ValueError("There should be exactly one site. Something is off.")
        cls.site = sites.first()

        cls.site.root_page = cls.homepage
        cls.site.clean()
        cls.site.save()

    @classmethod
    def _setup_locales(cls):
        cls.default_locale = wagtail_models.Locale.get_default()
        cls.fr_locale, _ = wagtail_models.Locale.objects.get_or_create(language_code="fr")
        cls.de_locale, _ = wagtail_models.Locale.objects.get_or_create(language_code="de")
        assert cls.fr_locale != cls.default_locale

    def setUp(self):
        super().setUp()
        self.activate_locale(self.default_locale)

    def synchronize_tree(self):
        synctree.synchronize_tree(source_locale=self.default_locale, target_locale=self.fr_locale)

    def activate_locale(self, locale):
        translation.activate(locale.language_code)

    def translate_page(self, page, locale):
        return self.client.post(
            reverse(
                "wagtail_localize:submit_page_translation",
                args=[page.id],
            ),
            {"locales": [locale.id]},
        )

    def translate_snippet(self, snippet, locale):
        return self.client.post(
            reverse(
                "wagtail_localize:submit_snippet_translation",
                args=[snippet._meta.app_label, snippet._meta.model_name, snippet.pk],
            ),
            {"locales": [locale.id]},
            follow=True,
        )
