from mezzanine.conf import settings

referrer_value = 'same-origin'

if settings.REFERRER_HEADER_VALUE:
    referrer_value = settings.REFERRER_HEADER_VALUE

class ReferrerMiddleware: 

        # def __init__(self, get_response):
        #     self.get_response = get_response

        # def __call__(self, request):
        # response = self.get_response(request)
    def process_response(self, request, response):
        response['Referrer-Policy'] = referrer_value
        print("wat")
        return response
