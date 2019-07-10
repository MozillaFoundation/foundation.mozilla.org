from django.http import HttpResponseNotFound
from django.shortcuts import render


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
    if request.site.hostname == 'mozillafestival.org':
        html = render(request, 'mozfest/404.html')
        return HttpResponseNotFound(html)
    else:
        html = render(request, '404.html')
        return HttpResponseNotFound(html)
