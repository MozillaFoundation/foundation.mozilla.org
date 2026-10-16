from types import SimpleNamespace

from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase
from django.utils import translation
from wagtail.models import Locale, Site

from foundation_cms.snippets.models import NewsletterSignup


class NewsletterSignupTemplateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.signup = NewsletterSignup.objects.create(
            name="Newsletter",
            cta_header="Stay informed",
            cta_description="News and updates",
            button_text="Subscribe",
            newsletter="existing-list",
            layout="expand_on_focus",
        )
        locale, _ = Locale.objects.get_or_create(language_code="fr")
        cls.french = cls.signup.copy_for_translation(locale)
        cls.french.cta_header = "Restez au courant"
        cls.french.button_text = "Abonnez-vous"
        cls.french.save()

    @staticmethod
    def render(template, **context):
        request = RequestFactory().get("/en/")
        request.site = Site.objects.first()
        return BeautifulSoup(render_to_string(template, context, request=request), "html.parser")

    def test_shared_form_preserves_content_and_accessible_controls(self):
        soup = self.render("patterns/components/_newsletter_signup_form.html", newsletter_signup=self.signup)
        root = soup.select_one("[data-newsletter-signup]")
        self.assertEqual(root["data-signup-id"], str(self.signup.pk))
        self.assertEqual(root["data-layout"], "expand_on_focus")
        self.assertEqual(root.select_one(".mzf-c-newsletter__heading").text, "Stay informed")
        self.assertEqual(root.select_one(".mzf-c-newsletter__description").text, "News and updates")
        self.assertEqual(root.select_one("button[type=submit]").get_text(strip=True), "Subscribe")
        self.assertEqual(len(root.select("form")), 1)
        self.assertIsNotNone(root.select_one("[data-newsletter-email-label]"))
        self.assertTrue(root.select_one("[name=email]").has_attr("required"))
        self.assertIsNotNone(root.select_one("[name=privacy]").find_parent("label"))
        self.assertTrue(root.select_one("button[type=submit]").has_attr("disabled"))
        for name in ("country", "language"):
            dropdown = root.select_one(f"[data-newsletter-dropdown={name}]")
            self.assertEqual(dropdown.select_one(f"[name={name}]")["type"], "hidden")
            self.assertEqual(dropdown.select_one("button")["aria-haspopup"], "listbox")
            self.assertEqual(dropdown.select_one("ul")["role"], "listbox")
        self.assertFalse(root.select("select"))
        for selector in (
            "[data-email-error]",
            "[data-privacy-error]",
            "[data-newsletter-error]",
            "[data-newsletter-success]",
            "[data-newsletter-expanded]",
        ):
            self.assertTrue(root.select_one(selector).has_attr("hidden"))
        self.assertIsNotNone(root.select_one('a[href="https://www.mozilla.org/privacy/websites/"]'))

    def test_expanded_layout_and_optional_description(self):
        self.signup.layout = "expanded"
        self.signup.cta_description = ""
        soup = self.render("patterns/components/_newsletter_signup_form.html", newsletter_signup=self.signup)
        self.assertIsNone(soup.select_one(".mzf-c-newsletter__description"))
        self.assertTrue(all(not node.has_attr("hidden") for node in soup.select("[data-newsletter-expanded]")))

    def test_body_block_resolves_localized_snippet(self):
        with translation.override("fr"):
            soup = self.render(
                "patterns/blocks/themes/default/newsletter_signup_block.html",
                self={"newsletter_signup": self.signup},
            )
        root = soup.select_one("[data-newsletter-signup]")
        self.assertEqual(root["data-signup-id"], str(self.french.pk))
        self.assertEqual(root["data-current-language"], "fr")
        self.assertEqual(root.select_one("button").get_text(strip=True), "Abonnez-vous")

    def test_both_footer_hosts_keep_selected_variant_and_localized_settings_fallback(self):
        settings = {"snippets": {"FooterNewsletterSignup": SimpleNamespace(newsletter_signup=self.signup)}}
        for template in ("patterns/components/footer.html", "patterns/components/footer/_footer_content.html"):
            with self.subTest(template=template), translation.override("fr"):
                fallback = self.render(template, settings=settings)
                selected = self.render(template, settings=settings, footer_newsletter_signup=self.signup)
                self.assertEqual(
                    fallback.select_one("[data-newsletter-signup]")["data-signup-id"], str(self.french.pk)
                )
                self.assertEqual(
                    selected.select_one("[data-newsletter-signup]")["data-signup-id"], str(self.signup.pk)
                )

    def test_snippet_preview_uses_shared_form(self):
        soup = self.render("patterns/components/previews/footer_newsletter_signup.html", object=self.signup)
        self.assertEqual(len(soup.select("[data-newsletter-signup]")), 1)
        self.assertEqual(soup.select_one("[data-newsletter-signup]")["data-signup-id"], str(self.signup.pk))
