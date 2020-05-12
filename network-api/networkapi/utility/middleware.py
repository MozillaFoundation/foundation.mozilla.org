from django.http.response import HttpResponseRedirectBase
from django.conf import settings

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
