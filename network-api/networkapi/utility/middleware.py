from django import http
from django.http.response import HttpResponseRedirectBase
from django.conf import settings

from wagtail.contrib.redirects.middleware import RedirectMiddleware
from wagtail.contrib.redirects.models import Redirect
from wagtail.core.models import Page

hostnames = settings.TARGET_DOMAINS
referrer_value = 'same-origin'

if settings.REFERRER_HEADER_VALUE:
    referrer_value = settings.REFERRER_HEADER_VALUE


class HttpResponseTemporaryRedirect(HttpResponseRedirectBase):
    status_code = 307


class ReferrerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Referrer-Policy'] = referrer_value
        return response


class XRobotsTagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Do not index this page in public search engine results
        # https://developers.google.com/search/reference/robots_meta_tag#xrobotstag
        response = self.get_response(request)
        response['X-Robots-Tag'] = 'noindex'
        return response


class LocalizeRedirectMiddleware(RedirectMiddleware):
    """
    Check for an existing Redirect object. If it exists, and the user a LANGUAGE_CODE setting in their
    request, then attempt to redirect the user to their preferred locale and the same page using the same
    slug.

    If the language_code requirement isn't satisfied, or the redirect doesn't exist, or a localized
    version of the target page doesn't exist, then default back to standard Wagtail redirect logic.
    """
    def process_response(self, request, response):
        response = super().process_response(request, response)

        if hasattr(request, 'LANGUAGE_CODE'):
            path = Redirect.normalise_path(request.get_full_path())

            try:
                redirect = Redirect.objects.get(old_path=path, redirect_page__isnull=False)
            except Redirect.DoesNotExist:
                return response

            try:
                # Find the new localized page with the same slug
                page = Page.objects.get(locale__language_code=request.LANGUAGE_CODE, slug=redirect.redirect_page.slug)
            except Page.DoesNotExist:
                return response

            if redirect.is_permanent:
                return http.HttpResponsePermanentRedirect(page.url)
            else:
                return http.HttpResponseRedirect(page.url)

        return response


class TargetDomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DOMAIN_REDIRECT_MIDDLEWARE_ENABLED:
            request_host = request.META['HTTP_HOST']
            protocol = 'https' if request.is_secure() else 'http'

            # Temporary Redirect prior to Mozilla Festival 2019 site launch
            if settings.MOZFEST_DOMAIN_REDIRECT_ENABLED:
                if request_host == 'www.mozillafestival.org' and request.get_full_path() == '/':
                    redirect_url = '{protocol}://{hostname}{path}'.format(
                        protocol=protocol,
                        hostname=hostnames[0],
                        path='/mozfest/'
                    )

                    return HttpResponseTemporaryRedirect(redirect_url)

            # Redirect to the first hostname listed in the config
            if request_host not in hostnames:
                redirect_url = '{protocol}://{hostname}{path}'.format(
                    protocol=protocol,
                    hostname=hostnames[0],
                    path=request.get_full_path()
                )

                return HttpResponseTemporaryRedirect(redirect_url)

        return self.get_response(request)
