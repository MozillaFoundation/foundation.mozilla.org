import logging

log = logging.getLogger("django.request")

class DebugHostHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log.warning(
            "HOST DEBUG get_host=%s HTTP_HOST=%s XFH=%s XFP=%s SECURE=%s",
            request.get_host(),
            request.META.get("HTTP_HOST"),
            request.META.get("HTTP_X_FORWARDED_HOST"),
            request.META.get("HTTP_X_FORWARDED_PROTO"),
            request.is_secure(),
        )
        print(request.get_host())
        print(request.META.get("HTTP_HOST"))
        print(request.META.get("HTTP_X_FORWARDED_HOST"))
        print(request.META.get("HTTP_X_FORWARDED_PROTO"))
        print(request.is_secure())

        return self.get_response(request)