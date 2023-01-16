import base64
import hashlib
import hmac
import json

from .models import TitoEvent


def _tito_event_from_request_dict(request_dict):
    """Given the decoded and parsed body of webhook request from Tito, return
    the appropriate TitoEvent if it exists.
    Return False if a matching TitoEvent does not exist."""

    event_details = request_dict["event"]
    event_url = f"{event_details['account_slug']}/{event_details['slug']}"
    try:
        return TitoEvent.objects.get(event_id=event_url)
    except TitoEvent.DoesNotExist:
        return False


def is_valid_tito_request(signature, request_body):
    request_dict = json.loads(request_body.decode())
    matching_event = _tito_event_from_request_dict(request_dict)
    if matching_event:
        secret = bytes(matching_event.security_token, "utf-8")
        signed = sign_tito_request(secret, request_body)
        return signature == signed
    else:
        return False


def sign_tito_request(secret, content):
    # https://ti.to/docs/api/admin#webhooks-verifying-the-payload
    return base64.b64encode(hmac.new(secret, content, digestmod=hashlib.sha256).digest()).decode("utf-8")


def has_signed_up_to_newsletter(request_dict):
    matching_event = _tito_event_from_request_dict(request_dict)

    if matching_event:
        answers = request_dict.get("answers", [])
        for answer in answers:
            if str(answer["question"]["id"]) == matching_event.newsletter_question_id and len(answer["response"]):
                return True

    return False
