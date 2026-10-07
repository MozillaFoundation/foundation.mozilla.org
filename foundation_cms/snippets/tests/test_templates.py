from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase
from django.utils.html import escapejs
from wagtail.models import Locale

from foundation_cms.snippets.models import DonateBanner

BANNER_TEMPLATE = "patterns/components/donate_banner/donate_banner.html"
HEAD_TEMPLATE = "patterns/components/donate_banner/_pencil_banner_head.html"


class PencilBannerTemplateTests(TestCase):
    def setUp(self):
        self.banner = DonateBanner.objects.create(
            name="Pencil",
            title="Make a Giving Tuesday gift",
            banner_style="pencil",
            locale=Locale.get_default(),
        )
        self.request = RequestFactory().get("/")
        self.request.csp_nonce = "test-nonce"

    def test_renders_title_link_and_dismiss_key(self):
        html = render_to_string(
            BANNER_TEMPLATE,
            {"banner": self.banner, "cta_button_data": {"donate-banner-cta-button": ""}},
        )

        self.assertIn('class="donate-pencil-banner"', html)
        self.assertIn("Make a Giving Tuesday gift", html)
        self.assertIn('href="?form=donate"', html)
        self.assertIn("Support Mozilla", html)
        self.assertIn("data-donate-banner-cta-button", html)
        self.assertIn(f'data-dismiss-key="{self.banner.translation_key}"', html)
        self.assertNotIn("donate-banner__inner-wrapper", html)

    def test_head_script_only_renders_for_pencil_banners(self):
        html = render_to_string(HEAD_TEMPLATE, {"donate_banner": self.banner, "request": self.request})
        self.assertIn(f"donate_pencil_banner_dismissed={escapejs(str(self.banner.translation_key))}", html)
        self.assertIn('nonce="test-nonce"', html)

        self.banner.banner_style = "pushdown"
        html = render_to_string(HEAD_TEMPLATE, {"donate_banner": self.banner, "request": self.request})
        self.assertNotIn("<script", html)
