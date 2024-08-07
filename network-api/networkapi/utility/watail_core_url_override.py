# THIS IS JUST wagtail.urls BUT WITH A MORE PERMISSIVE URL PATTERN
# TO ALLOW NON-SLUG URLS FROM MAKING IT INTO THE serve() FUNCTION

from django.conf import settings
from django.urls import re_path
from wagtail import views
from wagtail.coreutils import WAGTAIL_APPEND_SLASH

if WAGTAIL_APPEND_SLASH:
    # If WAGTAIL_APPEND_SLASH is True (the default value), we match a
    # (possibly empty) list of path segments ending in slashes.
    # CommonMiddleware will redirect requests without a trailing slash to
    # a URL with a trailing slash

    # OLD PATTERN: "\w or dashes only"
    # NEW PATTERN: "anything that isn't /, followed by /"
    serve_pattern = r"^((?:[^\/]+/)*)$"
else:
    # If WAGTAIL_APPEND_SLASH is False, allow Wagtail to serve pages on URLs
    # with and without trailing slashes

    # OLD PATTERN: "\w or dashes only"
    # NEW PATTERN: "anything that isn't a slash, followed by an optional /"
    serve_pattern = r"^([^\/]+\/?)$"


WAGTAIL_FRONTEND_LOGIN_TEMPLATE = getattr(settings, "WAGTAIL_FRONTEND_LOGIN_TEMPLATE", "wagtailcore/login.html")


urlpatterns = [
    # Front-end page views are handled through Wagtail's core.views.serve
    # mechanism
    re_path(serve_pattern, views.serve, name="wagtail_serve"),
]
