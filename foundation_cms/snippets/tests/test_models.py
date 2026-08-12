from django.test import TestCase
from wagtail.models import Locale, Page, Site

from foundation_cms.base.factories import ImageFactory
from foundation_cms.core.models import HomePage, SitewideDonateBannerPage
from foundation_cms.snippets.models import (
    DonateBanner,
    IllustratedNewsletterSignup,
    NewsletterSignup,
    NewsletterUnsubscribe,
)
from foundation_cms.snippets.models.newsletter_signup import FooterNewsletterSignup


class SnippetModelTests(TestCase):
    def test_donate_banner_can_be_saved_and_activated_for_a_site(self):
        banner = DonateBanner.objects.create(
            name="Year-end Donation Banner",
            foreground_image=ImageFactory(),
            locale=Locale.get_default(),
        )

        banner.refresh_from_db()

        self.assertEqual(str(banner), "Year-end Donation Banner")
        self.assertFalse(banner.is_active())

        site = Site.objects.get(is_default_site=True)
        home_page = self._add_page(
            Page.get_first_root_node(),
            HomePage,
            "Model Smoke Home",
            "model-smoke-home",
        )
        site.root_page = home_page
        site.save()
        donate_banner_page = SitewideDonateBannerPage(
            title="Donate Banner",
            slug="donate-banner",
            donate_banner=banner,
        )
        home_page.add_child(instance=donate_banner_page)

        banner.refresh_from_db()

        self.assertEqual(donate_banner_page.get_site(), site)
        self.assertTrue(banner.is_active())

    def test_illustrated_newsletter_signup_can_be_saved(self):
        signup = IllustratedNewsletterSignup.objects.create(
            name="Illustrated Newsletter",
            heading="Keep up with Mozilla",
            locale=Locale.get_default(),
        )

        signup.refresh_from_db()

        self.assertEqual(str(signup), "Illustrated Newsletter")
        self.assertEqual(signup.heading, "Keep up with Mozilla")

    def test_newsletter_signup_can_be_saved(self):
        signup = self._create_newsletter_signup("Main Newsletter")

        signup.refresh_from_db()

        self.assertEqual(str(signup), "Main Newsletter")
        self.assertEqual(signup.cta_header, "Stay informed")

    def test_footer_newsletter_signup_can_be_saved_for_a_site(self):
        site = Site.objects.get(is_default_site=True)
        signup = self._create_newsletter_signup("Footer Newsletter")
        settings = FooterNewsletterSignup.for_site(site)
        settings.newsletter_signup = signup
        settings.save()

        settings.refresh_from_db()

        self.assertEqual(settings.site, site)
        self.assertEqual(settings.newsletter_signup, signup)

    def test_newsletter_unsubscribe_can_be_saved(self):
        unsubscribe = NewsletterUnsubscribe.objects.create(
            name="Newsletter Unsubscribe",
            locale=Locale.get_default(),
        )

        unsubscribe.refresh_from_db()

        self.assertEqual(str(unsubscribe), "Newsletter Unsubscribe")
        self.assertEqual(unsubscribe.header, "Unsubscribe from our emails")

    def _create_newsletter_signup(self, name):
        return NewsletterSignup.objects.create(
            name=name,
            cta_header="Stay informed",
            locale=Locale.get_default(),
        )

    def _add_page(self, parent, model, title, slug):
        page = model(
            title=title,
            slug=slug,
            seo_title=title,
            search_description=f"{title} description.",
        )
        parent.add_child(instance=page)
        return page
