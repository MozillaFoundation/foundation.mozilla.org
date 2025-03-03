from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from wagtail.admin.viewsets import viewsets as wagtail_admin_viewsets
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.models import Locale
from wagtail.test.utils import WagtailTestUtils

from foundation_cms.legacy_cms.donate_banner.factory import DonateBannerFactory
from foundation_cms.legacy_cms.donate_banner.models import DonateBanner


class TestDonateBannerSnippetChooser(WagtailTestUtils, TestCase):
    def is_donate_banner_chooser_viewset(self, viewset):
        return viewset.model == DonateBanner and issubclass(viewset.__class__, ChooserViewSet)

    def get_chooser_viewset(self):
        # Get the last registered ChooserViewSet for the DonateBanner model.
        # Note: There can be multiple ChooserViewSets registered for a model.
        wagtail_admin_viewsets.populate()
        model_viewsets = [x for x in wagtail_admin_viewsets.viewsets if self.is_donate_banner_chooser_viewset(x)]
        return model_viewsets[-1]

    def setUp(self):
        # Get the chooser url from the viewsets registry.
        # Would have been easier to get from model.snippet_viewset, but
        # that does not work somehow.
        chooser_viewset = self.get_chooser_viewset()
        self.chooser_url = reverse(f"{chooser_viewset.name}:choose")

        User = get_user_model()
        self.user = User.objects.create_superuser("admin-user", "admin@example.com", "password")
        self.client.force_login(self.user)

        self.default_locale = Locale.get_default()
        self.fr_locale = Locale.objects.create(language_code="fr")
        self.banners = [
            DonateBannerFactory.create(name="Generic"),
            DonateBannerFactory.create(name="Easter"),
            DonateBannerFactory.create(name="Christmas"),
        ]

    def test_banner_chooser_exclude_locale(self):
        translated_banner = self.banners[0].copy_for_translation(self.fr_locale)
        translated_banner.save()
        all_banners = DonateBanner.objects.all()
        default_banners = DonateBanner.objects.filter(locale=self.default_locale)
        response = self.client.get(self.chooser_url)
        results = response.context["results"]

        # Chooser does not include every banner, but only the default langauge oness
        self.assertNotEqual(len(results), all_banners.count())
        self.assertEqual(len(results), default_banners.count())
        self.assertNotIn(translated_banner, results)
        self.assertIn(self.banners[0], results)

        # Banner chooser should not contain locale filter
        self.assertNotContains(response, "id_locale")
