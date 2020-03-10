from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils import translation


def custom404_view(request, exception):
    """
    This view handlers which 404 template to render, based on
    which host the request was a 404 for. We do this, because
    wagtail does not allow us to (currently) specify 404 pages
    using the site admin UI, so we need to rely on the Django
    methodology for handling 404 responses.

    It would be great if we could pull the "which domain uses
    which 404 template" information from the wagtail "sites"
    configuration, but there is no way to know which template
    belongs to which site, as "a site" is not tied to "a django
    app" in the wagtail way of things.
    """
    if request.site.hostname == 'www.mozillafestival.org':
        html = render(request, 'mozfest/404.html')
        return HttpResponseNotFound(html.content)
    else:
        html = render(request, '404.html')
        return HttpResponseNotFound(html.content)


def redirect_to_initiatives(request, subpath):
    lang = request.LANGUAGE_CODE
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    query_string = ""

    if request.META['QUERY_STRING']:
        query_string = f'?{request.META["QUERY_STRING"]}'

    return redirect(f'/{request.LANGUAGE_CODE}/initiatives/{subpath}{query_string}')
