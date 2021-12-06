import base64
import hashlib
import hmac
import json

import basket
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# To configure endpoints see:
# https://ti.to/Mozilla/mozilla-festival-2022/admin/settings/webhook_endpoints

@csrf_exempt
@require_POST
def tito_ticket_completed(request):
    # is it the correct webhook trigger?
    # https://ti.to/docs/api/admin#webhooks-triggers
    if not request.META.get("HTTP_X_WEBHOOK_NAME", "") == "ticket.completed":
        return HttpResponseBadRequest("Not a ticket completed request")

    # does the payload hash signature match
    # https://ti.to/docs/api/admin#webhooks-verifying-the-payload
    tito_signature = request.META.get("HTTP_TITO_SIGNATURE", "")
    secret = bytes(settings.TITO_SECURITY_TOKEN, "utf-8")
    signature = base64.b64encode(
        hmac.new(secret, request.body, digestmod=hashlib.sha256).digest()
    ).decode("utf-8")

    if tito_signature != signature:
        return HttpResponseBadRequest("Payload verification failed")

    # have they signed up to the newsletter?
    data = json.loads(request.body.decode())
    for answer in data.get("answers", []):
        if (
            answer["question"]["id"] == int(settings.TITO_NEWSLETTER_QUESTION_ID)
            and len(answer["response"])
            and data.get("email")
        ):
            basket.subscribe(data.get("email"), "mozilla-festival")

    return HttpResponse(status=202)
