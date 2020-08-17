import re
from django.conf import settings
from django.utils import translation


# Used to export env variable to Django templates
def review_app(request):
    return {'REVIEW_APP': settings.REVIEW_APP}


# Used in BuyersGuide templates to check if we're using cloudinary
def cloudinary(request):
    return {'USE_CLOUDINARY': settings.USE_CLOUDINARY}


def canonical_path(request):
    lang = getattr(request, 'locale', translation.get_language())
    url = getattr(request, 'path', '/')
    print(re.sub(r'^/' + lang, '', url))
    return {'CANONICAL_PATH': re.sub(r'^/' + lang, '', url)}


def canonical_site_url(request):
    return {'CANONICAL_SITE_URL': request.scheme + '://' + request.get_host()}
