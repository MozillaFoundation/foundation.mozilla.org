import json
import logging

import basket
import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from rest_framework import status
from wagtail.models import Site

from foundation_cms.legacy_apps.mozfest.models import MozfestHomepage
from foundation_cms.legacy_apps.wagtailpages.models import Homepage
from foundation_cms.snippets.models.newsletter_signup import NewsletterSignup

logger = logging.getLogger(__name__)


class EnvVariablesView(View):
    """
    A view that permits a GET to expose allowlisted environment
    variables in JSON.
    """

    def get(self, request):
        return JsonResponse(settings.FRONTEND)


def review_app_help_view(request):
    if settings.REVIEW_APP:
        return render(request, "reviewapp-help.html")
    else:
        return HttpResponse(status=404)


@require_GET
def apple_pay_domain_association_view(request):
    """
    Returns string needed for Apple Pay domain association/verification,
    based on which site is making the request.
    """
    request_site_root = Site.find_for_request(request).root_page.specific
    mozfest_key = settings.APPLE_PAY_DOMAIN_ASSOCIATION_KEY_MOZFEST
    foundation_key = settings.APPLE_PAY_DOMAIN_ASSOCIATION_KEY_FOUNDATION
    key_not_found_message = "Key not found. Please check environment variables."

    if isinstance(request_site_root, MozfestHomepage):
        if mozfest_key:
            response_contents = mozfest_key
            status_code = 200
        else:
            response_contents = key_not_found_message
            status_code = 501

    elif isinstance(request_site_root, Homepage):
        if foundation_key:
            response_contents = foundation_key
            status_code = 200
        else:
            response_contents = key_not_found_message
            status_code = 501

    else:
        response_contents = "Request site not recognized."
        status_code = 400

    return HttpResponse(response_contents, status=status_code, content_type="text/plain; charset=utf-8")


def process_lang_code(lang):
    # Salesforce expects "pt" instead of "pt-BR".
    # See https://github.com/mozilla/foundation.mozilla.org/issues/5993
    if lang == "pt-BR":
        return "pt"
    return lang


NEWSLETTER_ENDPOINTS = {
    "mozilla-foundation": settings.FOUNDATION_NEWSLETTER_ENDPOINT,
    "mozfest": settings.MOZFEST_NEWSLETTER_ENDPOINT,
    "common-voice": settings.COMMONVOICE_NEWSLETTER_ENDPOINT,
    "unsubscribe": settings.UNSUBSCRIBE_NEWSLETTER_ENDPOINT,
}

REQUEST_TIMEOUT_SECONDS = getattr(settings, "NEWSLETTER_SUBSCRIBE_TIMEOUT", 8)


@csrf_exempt
@require_http_methods(["POST"])
def newsletter_signup_submission_view(request, pk):
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
        signup = NewsletterSignup.objects.get(id=pk)
    except ObjectDoesNotExist:
        # Create a "default" Signup object, but without
        # actually saving that object to the database,
        # because we really just want to use it for getting
        # the default newsletter to sign up for.
        signup = NewsletterSignup()

    return newsletter_signup_submission(request, signup)


# handle newsletter signup data
def newsletter_signup_submission(request, signup):
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

    if newsletter == "unsubscribe":
        unsubscribe_request = requests.post(
            settings.UNSUBSCRIBE_NEWSLETTER_ENDPOINT,
            json={"email": email, "unsubscribe_all": True},
            headers={"X-API-Key": settings.EXISTING_NEWSLETTER_SUBSCRIPTION_CHECK_ENDPOINT_KEY},
            timeout=8,
        )

        if unsubscribe_request.status_code == 200:
            return JsonResponse({email: "test"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({email: "test"}, status=status.HTTP_400_BAD_REQUEST)

    else:

        # Make request to check if email is already subscribed
        lookup = requests.get(
            settings.EXISTING_NEWSLETTER_SUBSCRIPTION_CHECK_ENDPOINT,
            params={"email": email},
            headers={"X-API-Key": settings.EXISTING_NEWSLETTER_SUBSCRIPTION_CHECK_ENDPOINT_KEY},
            timeout=8,
        )

        # If user is already subscribed, return an error.
        if lookup.status_code == 200:
            return JsonResponse(
                {"status": "error", "message": "Already subscribed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if 404 or anything else, just proceed with normal subscription flow

        else:
            if not endpoint_url:
                return JsonResponse(
                    {"error": f"Unsupported newsletter '{newsletter}'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # rewrite payload
            data = {
                "email": email,
                "format": "html",
                "source_url": source,
                "newsletters": newsletter,
                "lang": process_lang_code(rq.get("lang", "en")),
                "country": rq.get("country", ""),
                # Empty string instead of None due to Basket issues
                "first_name": "",
                "last_name": "",
            }

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
                # New endpoint: doesn't want "newsletters"
                data.pop("newsletters", None)
                resp = requests.post(
                    endpoint_url,
                    json=data,
                    timeout=8,
                    headers={"Content-Type": "application/json"},
                )

                if resp.status_code == 200:
                    return JsonResponse(data, status=status.HTTP_201_CREATED)

                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
