import json

from django.test import TestCase
from django.urls import reverse
from wagtail.models import Page, Site

from foundation_cms.legacy_apps.events.factory import TitoEventFactory
from foundation_cms.legacy_apps.mozfest.factory import MozfestHomepageFactory


class TitoTicketCompletedTest(TestCase):
    def setUp(self):
        self.url = reverse("tito-ticket-completed")
        self.tito_event = TitoEventFactory.create()

    def _webhook_data(self):
        account_slug, slug = self.tito_event.event_id.split("/")
        return {"event": {"account_slug": account_slug, "slug": slug}}

    def test_incorrect_http_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_incorrect_webhook_name(self):
        response = self.client.post(
            self.url, data=self._webhook_data(), content_type="application/json", headers={"x-webhook-name": "invalid"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)["error"], "Not a ticket completed request")

    def test_missing_tito_signature(self):
        response = self.client.post(
            self.url,
            data=self._webhook_data(),
            content_type="application/json",
            headers={"x-webhook-name": "ticket.completed"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)["error"], "Payload verification failed")

    def test_invalid_tito_signature(self):
        response = self.client.post(
            self.url,
            data=self._webhook_data(),
            content_type="application/json",
            headers={"x-webhook-name": "ticket.completed", "tito-signature": "invalid"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)["error"], "Payload verification failed")


class TitoWidgetBlockLocalizationTest(TestCase):
    """
    Making sure that the tito widget block template is being sent a language code supported by Tito.
    If the user is visiting with an unsupported language, default to English.
    (List of supported languages can be found in TitoWidgetBlock model definition)
    """

    def setUp(self):
        # Setting up a mozfest site and homepage with a tito widget block.
        self.site = Site.objects.first()
        site_root = Page.objects.get(depth=1)
        self.mozfest_homepage = MozfestHomepageFactory.create(parent=site_root)
        self.mozfest_homepage.body = [
            ("tito_widget", {"button_label": "test widget", "styling": "btn-primary", "event": TitoEventFactory()})
        ]
        self.mozfest_homepage.save()
        self.site.root_page = self.mozfest_homepage
        self.site.save()

    def test_lang_code_with_default_language(self):
        # English is the site's default language, so get_url() on the mozfest homepage should
        # return "/en/", and the same language code should be sent to the tito widget block template.
        response = self.client.get(self.mozfest_homepage.get_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tito_widget_lang_code"], "en")
        self.assertTemplateUsed(response, template_name="wagtailpages/blocks/tito_widget_block.html")

    def test_lang_code_with_supported_non_default_language(self):
        # Since FR is a Tito supported language, the tito widget block
        # template should also be sent the language code "fr".
        response = self.client.get("/fr/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tito_widget_lang_code"], "fr")
        self.assertTemplateUsed(response, template_name="wagtailpages/blocks/tito_widget_block.html")

    def test_unsupported_language_defaults_to_english(self):
        # Since fy-NL is a not a Tito supported language, the tito widget block
        # template should default to the English language code "en".
        response = self.client.get("/fy-NL/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tito_widget_lang_code"], "en")
        self.assertTemplateUsed(response, template_name="wagtailpages/blocks/tito_widget_block.html")
