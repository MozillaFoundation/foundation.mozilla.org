import json
import logging

import basket
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from django.conf import settings
import requests

from foundation_cms.legacy_apps.wagtailpages.models import Signup


def process_lang_code(lang):
    # Salesforce expects "pt" instead of "pt-BR".
    # See https://github.com/mozilla/foundation.mozilla.org/issues/5993
    if lang == "pt-BR":
        return "pt"
    return lang


logger = logging.getLogger(__name__)


NEWSLETTER_ENDPOINTS = {
    "mozilla-foundation": settings.FOUNDATION_NEWSLETTER_ENDPOINT,
    "mozilla-festival": settings.MOZFEST_NEWSLETTER_ENDPOINT,
    "common-voice": settings.COMMONVOICE_NEWSLETTER_ENDPOINT,
    "unsubscribe": settings.UNSUBSCRIBE_NEWSLETTER_ENDPOINT,
}

REQUEST_TIMEOUT_SECONDS = getattr(settings, "NEWSLETTER_SUBSCRIBE_TIMEOUT", 8)



@csrf_exempt
@require_http_methods(["POST"])
def signup_submission_view(request, pk):
    # We need to re-write the data that's coming in from the network request.
    # Network request's send data through the request.body, not request.POST despite it being a POST method
    # request.POST is supported for unit tests
    new_body = request.body.decode("utf-8")
    try:
        request.data = json.loads(new_body)
    except ValueError:
        return JsonResponse(
            {
                "error": "Could not validate incoming data",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        signup = Signup.objects.get(id=pk)
    except ObjectDoesNotExist:
        # Create a "default" Signup object, but without
        # actually saving that object to the database,
        # because we really just want to use it for getting
        # the default newsletter to sign up for.
        signup = Signup()

    return signup_submission(request, signup)


# handle  newsletter signup data
def signup_submission(request, signup):
    rq = request.data

    # payload validation
    email = rq.get("email")
    if email is None:
        return JsonResponse(
            {"error": "Signup requires an email address"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    source = rq.get("source")
    if source is None:
        return JsonResponse(
            {"error": "Unknown source"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    newsletter = signup.newsletter.strip().lower()
    endpoint_url = NEWSLETTER_ENDPOINTS.get(newsletter)


    if not endpoint_url:
        return JsonResponse(
            {"error": f"Unsupported newsletter '{newsletter}'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # rewrite payload

    # rewrite payload for basket
    data = {
        "email": email,
        "format": "html",
        "source_url": source,
        "newsletters": newsletter,
        "lang": process_lang_code(rq.get("lang", "en")),
        "country": rq.get("country", ""),
        # Empty string instead of None due to Basket issues
        "first_name": rq.get("givenNames", ""),
        "last_name": rq.get("surname", ""),
    }

    # add the campaign id to this payload, if there is one.
    cid = signup.campaign_id
    if cid is not None and cid != "":
        data["campaign_id"] = cid

    newsletter_signup_method = getattr(settings, "NEWSLETTER_SIGNUP_METHOD", "BASKET")

    if newsletter_signup_method == "BASKET":
        # Subscribing to newsletter using basket.
        # https://basket-client.readthedocs.io/en/latest/usage.html
        basket_additional = {"lang": data["lang"], "source_url": data["source_url"]}
        if data["country"] != "":
            basket_additional["country"] = data["country"]

        response = basket.subscribe(data["email"], data["newsletters"], **basket_additional)

        if response["status"] == "ok":
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    else:
        print("Subscribing using direct POST")
        # New endpoint: doesn't want "newsletters"
        data.pop("newsletters", None)
        resp = requests.post(
            endpoint_url,
            json=data,
            timeout=8,
            headers={"Content-Type": "application/json"},
        )
        print(resp.status_code)
        print(resp.json())

        if resp.status_code == 200:
            return JsonResponse(data, status=status.HTTP_201_CREATED)

        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
