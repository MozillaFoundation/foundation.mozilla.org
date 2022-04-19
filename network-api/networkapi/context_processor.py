import re
from django.conf import settings
from django.utils import translation


# Used to export env variable to Django templates
def review_app(request):
    return {'REVIEW_APP': settings.REVIEW_APP}


def canonical_path(request):
    lang = getattr(request, 'locale', translation.get_language())
    url = getattr(request, 'path', '/')
    return {'CANONICAL_PATH': re.sub(r'^/' + lang, '', url)}


def canonical_site_url(request):
    return {'CANONICAL_SITE_URL': request.scheme + '://' + request.get_host()}
