import re

from django.conf import settings
from django.utils import translation


# Used to export env variable to Django templates
def review_app(request):
    return {"REVIEW_APP": settings.REVIEW_APP}


def canonical_path(request):
    lang = getattr(request, "locale", translation.get_language())
    url = getattr(request, "path", "/")
    return {"CANONICAL_PATH": re.sub(r"^/" + lang, "", url)}


def canonical_site_url(request):
    return {"CANONICAL_SITE_URL": request.scheme + "://" + request.get_host()}


def mozfest_schedule_url(request):
    return {"MOZFEST_SCHEDULE_URL": settings.MOZFEST_SCHEDULE_URL}


def editable_nav(request):
    return {"EDITABLE_NAV": settings.EDITABLE_NAV}
