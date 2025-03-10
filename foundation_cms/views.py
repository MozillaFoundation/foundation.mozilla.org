from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_GET
from wagtail.models import Site

from foundation_cms.legacy_apps.mozfest.models import MozfestHomepage
from foundation_cms.legacy_apps.wagtailpages.models import Homepage


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
