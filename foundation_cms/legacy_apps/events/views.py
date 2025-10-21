import json
import logging

import basket
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from foundation_cms.views import process_lang_code, subscribe_to_camo_newsletter

from .utils import has_signed_up_to_newsletter, is_valid_tito_request

logger = logging.getLogger(__name__)

# To configure endpoints see:
# https://ti.to/Mozilla/mozilla-festival-2022/admin/settings/webhook_endpoints


@csrf_exempt
@require_POST
def tito_ticket_completed(request):
    # is it the correct webhook trigger?
    # https://ti.to/docs/api/admin#webhooks-triggers
    if not request.headers.get("x-webhook-name", "") == "ticket.completed":
        return HttpResponseBadRequest("Not a ticket completed request")

    # does the payload hash signature match
    tito_signature = request.headers.get("tito-signature", "")
    if not is_valid_tito_request(tito_signature, request.body):
        return HttpResponseBadRequest("Payload verification failed")

    # have they signed up to the newsletter?
    data = json.loads(request.body.decode())
    email = data.get("email")

    if email and has_signed_up_to_newsletter(data):
        try:
            newsletter_signup_method = getattr(settings, "NEWSLETTER_SIGNUP_METHOD", "BASKET")

            # retain codeblock for basket subscribe
            if newsletter_signup_method == "BASKET":
                basket.subscribe(email, "mozilla-festival")

            # rewrite to camo based on foundation_cms/views.py
            # @TODO remove basket code, make this more DRY w/ views.py
            # @TODO we should have a separate ENV variable for dev CAMO endpoint
            else:
                # rewrite payload
                data = {
                    "email": email,
                    "format": "html",
                    "source_url": request.source,
                    "newsletters": "tito",
                    "lang": process_lang_code(request.get("lang", "en")),
                    "country": request.get("country", ""),
                    # Empty string instead of None due to Basket issues
                    "first_name": "",
                    "last_name": "",
                }
                return subscribe_to_camo_newsletter(data)

        except Exception as error:
            logger.exception(f"Subscription from Tito webhook failed: {str(error)}")

    return HttpResponse(status=202)
