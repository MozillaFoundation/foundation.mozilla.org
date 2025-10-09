from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.utils import translation
from wagtail.models import Site

from foundation_cms.core.models.home_page import HomePage as RedesignHomePage


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

    site = Site.find_for_request(request)

    if site.hostname == "www.mozillafestival.org":
        html = render(request, "mozfest/404.html")

    else:
        site_root = site.root_page.specific
        if isinstance(site_root, RedesignHomePage):
            parent_homepage = "redesign"
        else:
            parent_homepage = "legacy"
        context = {
            "parent_homepage": parent_homepage,
        }
        html = render(request, "404.html", context)

    return HttpResponseNotFound(html.content)


def localized_redirect(request, subpath, destination_path):
    lang = request.LANGUAGE_CODE
    translation.activate(lang)
    query_string = ""

    if request.META["QUERY_STRING"]:
        query_string = f'?{request.META["QUERY_STRING"]}'

    return redirect(f"/{request.LANGUAGE_CODE}/{destination_path}/{subpath}{query_string}")
