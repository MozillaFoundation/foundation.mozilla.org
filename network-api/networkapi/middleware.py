from mezzanine.conf import settings
from django.utils.deprecation import MiddlewareMixin

referrer_value = 'same-origin'

if settings.REFERRER_HEADER_VALUE:
    referrer_value = settings.REFERRER_HEADER_VALUE


class ReferrerMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Referrer-Policy'] = referrer_value
        return response
