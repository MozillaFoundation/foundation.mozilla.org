import json
from unittest import mock

from django.urls import reverse
from django.test import RequestFactory, TestCase, override_settings

from .views import tito_ticket_completed
from .utils import sign_tito_request


TITO_SECURITY_TOKEN = "abcdef123456"
TITO_NEWSLETTER_QUESTION_ID = 123456


@override_settings(
    TITO_SECURITY_TOKEN=TITO_SECURITY_TOKEN,
    TITO_NEWSLETTER_QUESTION_ID=TITO_NEWSLETTER_QUESTION_ID,
)
class TitoTicketCompletedTest(TestCase):
    def setUp(self):
        self.url = reverse("tito-ticket-completed")

    def test_incorrect_http_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_incorrect_webhook_name(self):
        response = self.client.post(self.url, data={}, HTTP_X_WEBHOOK_NAME="invalid")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Not a ticket completed request")

    def test_missing_tito_signature(self):
        response = self.client.post(
            self.url, data={}, HTTP_X_WEBHOOK_NAME="ticket.completed"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Payload verification failed")

    def test_invalid_tito_signature(self):
        response = self.client.post(
            self.url,
            data={},
            HTTP_X_WEBHOOK_NAME="ticket.completed",
            HTTP_TITO_SIGNATURE="invalid",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Payload verification failed")

    @mock.patch("networkapi.events.views.basket")
    def test_calls_basket_api(self, mock_basket):
        secret = bytes(TITO_SECURITY_TOKEN, "utf-8")
        data = {
            "answers": [
                {
                    "question": {"id": TITO_NEWSLETTER_QUESTION_ID},
                    "response": ["yes"],
                },
            ],
            "email": "rich@test.com",
        }

        factory = RequestFactory()
        request = factory.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
            HTTP_X_WEBHOOK_NAME="ticket.completed",
        )
        request.META["HTTP_TITO_SIGNATURE"] = sign_tito_request(secret, request.body)

        response = tito_ticket_completed(request)

        self.assertEqual(response.status_code, 202)
        mock_basket.subscribe.assert_called_once_with(
            "rich@test.com", "mozilla-festival"
        )

    def test_logs_basket_exception(self):
        # Using `failure@example.com` as the email causes an exception, see:
        # https://github.com/mozilla/basket-example#tips

        secret = bytes(TITO_SECURITY_TOKEN, "utf-8")
        data = {
            "answers": [
                {
                    "question": {"id": TITO_NEWSLETTER_QUESTION_ID},
                    "response": ["yes"],
                },
            ],
            "email": "failure@example.com",
        }

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
