from django.conf import settings
from django.http import JsonResponse, HttpResponse
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
    if settings.REVIEW_APP:
        return render(request, 'reviewapp-help.html')
    else:
        return HttpResponse(status=404)


def YoutubeRegrets2021View(request):
   return render(request, 'wagtailpages/pages/youtube-regrets-2021/youtube_regrets_2021.html')
