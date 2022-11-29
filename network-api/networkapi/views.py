from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_GET

from wagtail.core.models import Site


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
    Returns key needed for Apple Pay domain association/verification.
    """
    if Site.find_for_request(request).hostname == "www.mozillafestival.org":
        verification_key = settings.APPLE_PAY_DOMAIN_ASSOCIATION_KEY_MOZFEST
    else:
        verification_key = settings.APPLE_PAY_DOMAIN_ASSOCIATION_KEY_FOUNDATION
    return HttpResponse(verification_key, content_type="text/plain")
