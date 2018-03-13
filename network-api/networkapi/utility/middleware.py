from django.http.response import HttpResponseRedirectBase
from mezzanine.conf import settings

hostname = settings.TARGET_DOMAIN


class HttpResponseTemporaryRedirect(HttpResponseRedirectBase):
    status_code = 307


class TargetDomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DOMAIN_REDIRECT_MIDDLWARE_ENABLED:
            request_host = request.META['HTTP_HOST']

            if request_host != hostname:
                protocol = 'https' if request.is_secure() else 'http'

                redirect_url = '{protocol}://{hostname}{path}'.format(
                    protocol=protocol,
                    hostname=hostname,
                    path=request.get_full_path()
                )

                return HttpResponseTemporaryRedirect(redirect_url)

        return self.get_response(request)
