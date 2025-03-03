import json
from unittest import mock

from django.test import RequestFactory, TestCase
from django.urls import reverse
from wagtail.models import Page, Site

from foundation_cms.legacy_cms.events.factory import TitoEventFactory
from foundation_cms.legacy_cms.events.utils import sign_tito_request
from foundation_cms.legacy_cms.events.views import tito_ticket_completed
from foundation_cms.legacy_cms.mozfest.factory import MozfestHomepageFactory


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
        self.assertEqual(response.content.decode(), "Not a ticket completed request")

    def test_missing_tito_signature(self):
        response = self.client.post(
            self.url,
            data=self._webhook_data(),
            content_type="application/json",
            headers={"x-webhook-name": "ticket.completed"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Payload verification failed")

    def test_invalid_tito_signature(self):
        response = self.client.post(
            self.url,
            data=self._webhook_data(),
            content_type="application/json",
            headers={"x-webhook-name": "ticket.completed", "tito-signature": "invalid"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Payload verification failed")

    @mock.patch("foundation_cms.legacy_cms.events.views.basket")
    def test_calls_basket_api(self, mock_basket):
        secret = bytes(self.tito_event.security_token, "utf-8")
        data = {
            "answers": [
                {
                    "question": {"id": self.tito_event.newsletter_question_id},
                    "response": ["yes"],
                },
            ],
            "email": "rich@test.com",
        } | self._webhook_data()

        factory = RequestFactory()
        request = factory.post(
            self.url,
            data=data,
            content_type="application/json",
            HTTP_X_WEBHOOK_NAME="ticket.completed",
        )
        request.META["HTTP_TITO_SIGNATURE"] = sign_tito_request(secret, request.body)

        response = tito_ticket_completed(request)

        self.assertEqual(response.status_code, 202)
        mock_basket.subscribe.assert_called_once_with("rich@test.com", "mozilla-festival")

    def test_logs_basket_exception(self):
        # Using `failure@example.com` as the email causes an exception, see:
        # https://github.com/mozilla/basket-example#tips

        secret = bytes(self.tito_event.security_token, "utf-8")
        data = {
            "answers": [
                {
                    "question": {"id": self.tito_event.newsletter_question_id},
                    "response": ["yes"],
                },
            ],
            "email": "failure@example.com",
        } | self._webhook_data()

        factory = RequestFactory()
        request = factory.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
            HTTP_X_WEBHOOK_NAME="ticket.completed",
        )
        request.META["HTTP_TITO_SIGNATURE"] = sign_tito_request(secret, request.body)

        with self.assertLogs(logger="foundation_cms.legacy_cms.events.views", level="ERROR") as cm:
            response = tito_ticket_completed(request)
            self.assertEqual(response.status_code, 202)
            self.assertIn("Basket subscription from Tito webhook failed", cm.output[0])


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
