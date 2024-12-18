from django.conf import settings
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

hostnames = settings.TARGET_DOMAINS

if len(hostnames) == 0:
    print("Error: no TARGET_DOMAINS set, please ensure your environment variables are in order.")


class HttpResponseTemporaryRedirect(HttpResponseRedirectBase):
    status_code = 307


class XRobotsTagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Do not index this page in public search engine results
        # https://developers.google.com/search/reference/robots_meta_tag#xrobotstag
        response = self.get_response(request)
        response["X-Robots-Tag"] = "noindex"
        return response


class TargetDomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DOMAIN_REDIRECT_MIDDLEWARE_ENABLED:
            request_host = request.headers["host"]
            protocol = "https" if request.is_secure() else "http"

            # Temporary Redirect prior to Mozilla Festival 2019 site launch
            if settings.MOZFEST_DOMAIN_REDIRECT_ENABLED:
                if request_host == "www.mozillafestival.org" and request.get_full_path() == "/":
                    redirect_url = "{protocol}://{hostname}{path}".format(
                        protocol=protocol, hostname=hostnames[0], path="/mozfest/"
                    )

                    return HttpResponseTemporaryRedirect(redirect_url)

            # Redirect to the first hostname listed in the config
            if request_host not in hostnames:
                redirect_url = "{protocol}://{hostname}{path}".format(
                    protocol=protocol,
                    hostname=hostnames[0],
                    path=request.get_full_path(),
                )

                return HttpResponseTemporaryRedirect(redirect_url)

        return self.get_response(request)


# Middleware to normalize the pt-br and fy-nl locales to their capitalized regions (pt-BR and fy-NL)
class NormalizeLocaleMiddleware(MiddlewareMixin):
    # Dictionary mapping incorrect locale keys to their normalized forms
    locales_to_normalize = {"pt-br": "pt-BR", "fy-nl": "fy-NL"}

    def process_request(self, request):
        # Split the path into segments
        path_segments = request.path_info.strip("/").split("/")

        # Check if the first segment is a locale that needs to be normalized
        if len(path_segments) > 0 and path_segments[0] in self.locales_to_normalize:
            normalized_locale = self.locales_to_normalize[path_segments[0]]
            # Only redirect if the current locale is not already in the correct form
            if path_segments[0] != normalized_locale:
                path_segments[0] = normalized_locale
                new_path = "/" + "/".join(path_segments) + "/"  # Ensure trailing slash

                # Preserve query parameters if they exist
                query_string = request.META.get("QUERY_STRING")
                if query_string:
                    new_path += f"?{query_string}"

                return redirect(new_path, permanent=False)  # Using temporary redirects

        return None
