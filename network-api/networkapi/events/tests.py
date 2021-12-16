import base64
import hashlib
import hmac
import json

from django.urls import reverse
from django.test import RequestFactory, TestCase, override_settings

TITO_SECURITY_TOKEN = "abcdef123456"


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

    @override_settings(TITO_SECURITY_TOKEN=TITO_SECURITY_TOKEN)
    def test_calls_basket_api(self):
        from .views import tito_ticket_completed

        secret = bytes(TITO_SECURITY_TOKEN, "utf-8")
        data = {"answers": []}

        factory = RequestFactory()
        request = factory.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_WEBHOOK_NAME="ticket.completed",
        )

        signature = base64.b64encode(
            hmac.new(secret, request.body, digestmod=hashlib.sha256).digest()
        ).decode("utf-8")
        request.META["HTTP_TITO_SIGNATURE"] = signature

        response = tito_ticket_completed(request)
        self.assertEqual(response.status_code, 202)
