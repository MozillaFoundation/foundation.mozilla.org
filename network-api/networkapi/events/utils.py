import base64
import hashlib
import hmac
import json

from django.conf import settings
from .models import TitoEvent


def is_valid_tito_request(signature, request_body):
    event_details = json.loads(request_body.decode())['event']
    event_url = f"{event_details['account_slug']}/{event_details['slug']}"
    try:
        matching_event = TitoEvent.objects.get(event_id=event_url)
        secret = bytes(matching_event.security_token, "utf-8")
        data = json.loads(request.body.decode())
        signed = sign_tito_request(secret, request_body)
    except TitoEvent.DoesNotExist:
        # If there's no matching event, consider this request invalid
        return False

    return signature == signed


def sign_tito_request(secret, content):
    # https://ti.to/docs/api/admin#webhooks-verifying-the-payload
    return base64.b64encode(hmac.new(secret, content, digestmod=hashlib.sha256).digest()).decode("utf-8")


def has_signed_up_to_newsletter(tito_answers):
    for answer in tito_answers:
        if answer["question"]["id"] == int(settings.TITO_NEWSLETTER_QUESTION_ID) and len(answer["response"]):
            return True

    return False
