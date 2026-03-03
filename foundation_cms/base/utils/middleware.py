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
        if request.path.startswith("/cms/snippets/navigation/navigationmenu/preview/"):
            print("PATH", request.get_full_path())
            print("get_host()", request.get_host())
            print("HTTP_HOST", request.META.get("HTTP_HOST"))
            print("X_FWD_HOST", request.META.get("HTTP_X_FORWARDED_HOST"))
            print("X_ORIG_HOST", request.META.get("HTTP_X_ORIGINAL_HOST"))
            print("FORWARDED", request.META.get("HTTP_FORWARDED"))
            print("X_FWD_PROTO", request.META.get("HTTP_X_FORWARDED_PROTO"))
            
        return self.get_response(request)