from django.http import JsonResponse
from django.views import View
from mezzanine.conf import settings


class EnvVariablesView(View):
    """
    A view that permits a GET to expose whitelisted environment variables in JSON.
    """

    def get(self):
        return JsonResponse(settings.FRONTEND)
