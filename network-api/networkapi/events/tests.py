import json
from unittest import mock

from django.test import RequestFactory, TestCase
from django.urls import reverse

from .factory import TitoEventFactory
from .utils import sign_tito_request
from .views import tito_ticket_completed


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
            self.url, data=self._webhook_data(), content_type="application/json", HTTP_X_WEBHOOK_NAME="invalid"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Not a ticket completed request")

    def test_missing_tito_signature(self):
        response = self.client.post(
            self.url,
            data=self._webhook_data(),
            content_type="application/json",
            HTTP_X_WEBHOOK_NAME="ticket.completed",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Payload verification failed")

    def test_invalid_tito_signature(self):
        response = self.client.post(
            self.url,
            data=self._webhook_data(),
            content_type="application/json",
            HTTP_X_WEBHOOK_NAME="ticket.completed",
            HTTP_TITO_SIGNATURE="invalid",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Payload verification failed")

    @mock.patch("networkapi.events.views.basket")
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

        with self.assertLogs(logger="networkapi.events.views", level="ERROR") as cm:
            response = tito_ticket_completed(request)
            self.assertEqual(response.status_code, 202)
            self.assertIn("Basket subscription from Tito webhook failed", cm.output[0])
