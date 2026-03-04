from django.test import TestCase
from wagtail import models as wagtail_models

from foundation_cms.footer import factories as footer_factories
from foundation_cms.footer import models as footer_models


class SiteFooterTests(TestCase):
    """Tests for SiteFooter model."""

    def test_factory_creates_footer_with_links(self):
        """Factory should create a complete footer with all link types."""
        footer = footer_factories.SiteFooterFactory()

        self.assertIsInstance(footer, footer_models.SiteFooter)
        self.assertEqual(footer.internal_links.count(), 4)
        self.assertEqual(footer.external_links.count(), 5)
        self.assertEqual(footer.social_links.count(), 5)

    def test_footer_str(self):
        """Footer __str__ returns title."""
        footer = footer_factories.SiteFooterFactory(title="Test Footer")
        self.assertEqual(str(footer), "Test Footer")


class SiteFooterSettingsTests(TestCase):
    """Tests for SiteFooterSettings model."""

    def test_can_activate_footer_for_site(self):
        """Site settings should allow selecting an active footer."""
        footer = footer_factories.SiteFooterFactory()
        site = wagtail_models.Site.objects.first()

        settings = footer_models.SiteFooterSettings.for_site(site)
        settings.active_footer = footer
        settings.save()

        settings.refresh_from_db()
        self.assertEqual(settings.active_footer, footer)


class FooterLinkTests(TestCase):
    """Tests for footer link models."""

    def test_social_link_properties(self):
        """Social links should provide icon_class and aria_label."""
        footer = footer_factories.SiteFooterFactory()
        social = footer.social_links.filter(platform="instagram").first()

        self.assertEqual(social.icon_class, "icon-instagram")
        self.assertEqual(social.aria_label, "Instagram")
