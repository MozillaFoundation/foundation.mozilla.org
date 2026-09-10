from wagtail import models as wagtail_models
from wagtail_localize.fields import SynchronizedField

from foundation_cms.legacy_apps.mozfest.factory import MozfestPrimaryPageFactory
from foundation_cms.legacy_apps.mozfest.models import (
    MozfestHomepage,
    MozfestLandingPage,
    MozfestPrimaryPage,
)
from foundation_cms.legacy_apps.mozfest.tests.base import MozfestBaseTests
from foundation_cms.legacy_apps.wagtailpages.factory.signup import SignupFactory
from foundation_cms.snippets.factories import NoticeBannerFactory


class MozfestNoticeBannerTests(MozfestBaseTests):
    def test_mozfest_page_types_declare_synchronized_notice_banner(self):
        for page_model in (MozfestPrimaryPage, MozfestHomepage, MozfestLandingPage):
            synchronized_fields = {
                field.field_name for field in page_model.translatable_fields if isinstance(field, SynchronizedField)
            }
            self.assertIn("notice_banner", synchronized_fields)

    def test_promote_panels_include_notice_banner(self):
        panel_names = []
        for panel in MozfestPrimaryPage.promote_panels:
            field_name = getattr(panel, "field_name", None)
            if field_name:
                panel_names.append(field_name)
            for child in getattr(panel, "children", []) or []:
                panel_names.append(getattr(child, "field_name", type(child).__name__))

        self.assertIn("notice_banner", panel_names)

    def test_get_notice_banner_returns_localized_banner(self):
        banner = NoticeBannerFactory(body_text="Mozfest notice")
        page = MozfestPrimaryPageFactory(parent=self.mozfest_homepage, notice_banner=banner)

        self.assertEqual(page.get_notice_banner(), banner.localized)

    def test_page_renders_notice_banner(self):
        site = wagtail_models.Site.objects.get(is_default_site=True)
        site.root_page = self.mozfest_homepage
        site.save()

        SignupFactory(name="mozfest", locale=self.default_locale)
        banner = NoticeBannerFactory(body_text="Visible mozfest notice")
        page = MozfestPrimaryPageFactory(parent=self.mozfest_homepage, notice_banner=banner)
        page.save_revision().publish()

        response = self.client.get(page.url)

        self.assertContains(response, "notice-banner")
        self.assertContains(response, "Visible mozfest notice")
        self.assertTemplateUsed(response, "patterns/components/notice_banner/notice_banner.html")
