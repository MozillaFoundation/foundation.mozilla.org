from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views import View


class EnvVariablesView(View):
    """
    A view that permits a GET to expose whitelisted environment
    variables in JSON.
    """

    def get(self, request):
        return JsonResponse(settings.FRONTEND)


def review_app_help_view(request):
    try:
        if settings.HEROKU_APP_NAME:
            return render(request, 'reviewapp-help.html')
    except AttributeError:
        raise Http404()
