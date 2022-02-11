import base64
import hashlib
import hmac

from django.conf import settings


def is_valid_tito_request(signature, request_body):
    secret = bytes(settings.TITO_SECURITY_TOKEN, "utf-8")
    signed = sign_tito_request(secret, request_body)

    return signature == signed


def sign_tito_request(secret, content):
    # https://ti.to/docs/api/admin#webhooks-verifying-the-payload
    return base64.b64encode(
        hmac.new(secret, content, digestmod=hashlib.sha256).digest()
    ).decode("utf-8")


def has_signed_up_to_newsletter(tito_answers):
    for answer in tito_answers:
        if answer["question"]["id"] == int(
            settings.TITO_NEWSLETTER_QUESTION_ID
        ) and len(answer["response"]):
            return True

    return False
