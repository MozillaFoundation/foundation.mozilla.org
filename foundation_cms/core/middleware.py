from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation.trans_real import (
    check_for_language,
    get_language_from_path,
    get_supported_language_variant,
)
from wagtail.models import Locale


class PreferredLocaleRedirectMiddleware:
    excluded_prefixes = (
        "/cms/",
        "/admin/",
        "/api/",
        "/documents/",
        "/i18n/",
        "/static/",
        "/media/",
        "/pattern-library/",
        "/__debug__/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self._should_redirect(request):
            return self.get_response(request)

        language_code = self._get_preferred_language(request)

        if not language_code or language_code == settings.LANGUAGE_CODE:
            return self.get_response(request)

        localized_path = f"/{language_code}{request.get_full_path()}"

        return redirect(localized_path, permanent=False)

    def _should_redirect(self, request):
        return (
            request.method in {"GET", "HEAD"}
            and get_language_from_path(request.path_info) is None
            and not request.path_info.startswith(self.excluded_prefixes)
        )

    def _get_preferred_language(self, request):
        language_code = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

        if not language_code or not check_for_language(language_code):
            return None

        try:
            language_code = get_supported_language_variant(language_code)
        except LookupError:
            return None

        if not Locale.objects.filter(language_code=language_code).exists():
            return None

        return language_code
