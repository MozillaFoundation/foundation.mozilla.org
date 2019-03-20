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


class TargetDomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DOMAIN_REDIRECT_MIDDLEWARE_ENABLED:
            request_host = request.META['HTTP_HOST']

            # Redirect to the first hostname listed in the config
            if request_host not in hostnames:
                protocol = 'https' if request.is_secure() else 'http'

                redirect_url = '{protocol}://{hostname}{path}'.format(
                    protocol=protocol,
                    hostname=hostnames[0],
                    path=request.get_full_path()
                )

                return HttpResponseTemporaryRedirect(redirect_url)

        return self.get_response(request)
