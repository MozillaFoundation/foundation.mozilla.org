from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail.models import Locale
from wagtail_localize.fields import SynchronizedField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage
from foundation_cms.blocks.link_button_block import LinkButtonBlock
from foundation_cms.legacy_apps.wagtailpages.factory import blog as blog_factory
from foundation_cms.legacy_apps.wagtailpages.factory.primary_page import (
    PrimaryPageFactory,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.blog.blog import BlogPage
from foundation_cms.legacy_apps.wagtailpages.pagemodels.campaigns import (
    BanneredCampaignPage,
)
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base
from foundation_cms.snippets.factories import NoticeBannerFactory
from foundation_cms.snippets.models.notice_banner import NoticeBanner


class LinkButtonBlockTemplateTest(TestCase):
    def test_link_type_icon_rendering_is_opt_in(self):
        block = LinkButtonBlock()
        value = block.to_python(
            {
                "label": "External link",
                "link_to": "external_url",
                "external_url": "https://example.com/",
                "style": "btn-secondary",
                "alignment": "link-button-block--left",
            }
        )

        html = block.render(value)

        self.assertNotIn("link-type-icon", html)
        self.assertNotIn(" external", html)


class NoticeBannerFactoryTest(TestCase):
    def test_factory_creates_valid_notice_banner(self):
        banner = NoticeBannerFactory()

        banner.full_clean()
        self.assertTrue(NoticeBanner.objects.filter(pk=banner.pk).exists())
        self.assertEqual(banner.locale, Locale.get_default())

    def test_body_is_required(self):
        banner = NoticeBanner(name="Missing body", locale=Locale.get_default())

        with self.assertRaises(ValidationError):
            banner.full_clean()


class NoticeBannerPageIntegrationTest(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.blog_index = blog_factory.BlogIndexPageFactory(parent=cls.homepage)
        cls.blog_page = blog_factory.BlogPageFactory(parent=cls.blog_index)
        cls.primary_page = PrimaryPageFactory(parent=cls.homepage)

    def test_get_notice_banner_returns_none_when_unset(self):
        self.assertIsNone(self.blog_page.notice_banner_id)
        self.assertIsNone(self.blog_page.get_notice_banner())

    def test_get_notice_banner_returns_localized_banner(self):
        banner = NoticeBannerFactory(body_text="Localized notice body")
        self.blog_page.notice_banner = banner
        self.blog_page.save()

        self.assertEqual(self.blog_page.get_notice_banner(), banner.localized)

    def test_page_renders_notice_banner(self):
        banner = NoticeBannerFactory(body_text="Visible notice content")
        self.blog_page.notice_banner = banner
        self.blog_page.save_revision().publish()

        response = self.client.get(self.blog_page.url)

        self.assertContains(response, "notice-banner")
        self.assertContains(response, "Visible notice content")
        self.assertTemplateUsed(response, "patterns/components/notice_banner/notice_banner.html")

    def test_page_renders_notice_banner_cta_style_and_alignment(self):
        for style, alignment, link_type, link_value, icon_class in [
            (
                "btn-primary",
                "link-button-block--center",
                "external_url",
                "https://example.com/",
                "external",
            ),
            (
                "btn-secondary",
                "link-button-block--left",
                "email",
                "hello@example.com",
                "email",
            ),
            (
                "btn-secondary",
                "link-button-block--left",
                "relative_url",
                "/about/",
                "link",
            ),
        ]:
            with self.subTest(style=style, alignment=alignment, link_type=link_type):
                banner = NoticeBannerFactory(
                    body_text="Notice with a call to action",
                    cta=[
                        (
                            "link_button",
                            {
                                "label": "Learn more",
                                "link_to": link_type,
                                link_type: link_value,
                                "style": style,
                                "alignment": alignment,
                            },
                        )
                    ],
                )
                self.blog_page.notice_banner = banner
                self.blog_page.save_revision().publish()

                response = self.client.get(self.blog_page.url)

                self.assertContains(response, f'class="link-button-block {alignment}"')
                self.assertContains(response, f'class="{style}')
                self.assertContains(response, "link-button link-type-icon")
                self.assertContains(response, f"link-type-icon {icon_class}")
                expected_href = f"mailto:{link_value}" if link_type == "email" else link_value
                self.assertContains(response, f'href="{expected_href}"')
                self.assertContains(response, "Learn more")

    def test_page_without_notice_banner_does_not_render_markup(self):
        response = self.client.get(self.primary_page.url)

        self.assertNotContains(response, "notice-banner")

    def test_deleting_notice_banner_nulls_page_relation(self):
        banner = NoticeBannerFactory()
        self.blog_page.notice_banner = banner
        self.blog_page.save()

        banner.delete()
        self.blog_page.refresh_from_db()

        self.assertIsNone(self.blog_page.notice_banner_id)

    def test_notice_banner_is_synchronized_on_page_translation(self):
        banner = NoticeBannerFactory()
        self.blog_page.notice_banner = banner
        self.blog_page.save_revision().publish()

        self.homepage.copy_for_translation(self.fr_locale)
        self.blog_index.copy_for_translation(self.fr_locale)
        fr_page = self.blog_page.copy_for_translation(self.fr_locale)
        fr_page.save_revision().publish()

        self.assertEqual(fr_page.notice_banner_id, banner.id)

    def test_blog_page_and_abstract_base_page_declare_synchronized_notice_banner(self):
        blog_fields = {
            field.field_name for field in BlogPage.translatable_fields if isinstance(field, SynchronizedField)
        }
        abstract_fields = {
            field.field_name for field in AbstractBasePage.translatable_fields if isinstance(field, SynchronizedField)
        }

        self.assertIn("notice_banner", blog_fields)
        self.assertIn("notice_banner", abstract_fields)

    def test_bannered_campaign_page_promote_panels_include_notice_banner(self):
        panel_names = []
        for panel in BanneredCampaignPage.promote_panels:
            field_name = getattr(panel, "field_name", None)
            if field_name:
                panel_names.append(field_name)
            for child in getattr(panel, "children", []) or []:
                panel_names.append(getattr(child, "field_name", type(child).__name__))

        self.assertIn("notice_banner", panel_names)
