from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation import trans_real
from wagtail.models import Locale


class PreferredLocaleRedirectMiddleware:
    """
    Middleware to redirect users to their preferred locale using the language cookie if locale is not
    specified in the URL.
    - URLs that start with any of the excluded prefixes will not be redirected.
    - URLs that already have a locale prefix will not be redirected.
    - If the language cookie is not set or does not correspond to a valid Locale, no redirection will occur.
    - If the language cookie corresponds to the default language(settings.LANGUAGE_CODE), no redirection will occur.
    - If the language cookie corresponds to a valid Locale, the user will be redirected to the same URL with the
      locale prefix added.
    """

    locale_aliases = {
        "pt": "pt-BR",
    }

    excluded_prefixes = (
        "/cms",
        "/admin",
        "/api",
        "/documents",
        "/i18n",
        "/jsi18n",
        "/static",
        "/soc",
        "/media",
        "/pattern-library",
        "/__debug__",
        "/robots.txt",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self._should_redirect(request):
            return self.get_response(request)

        language_code = self._get_preferred_language(request)
        if not language_code or language_code == settings.LANGUAGE_CODE:
            return self.get_response(request)

        return redirect(
            f"/{language_code}{request.get_full_path()}",
            permanent=False,
        )

    def _should_redirect(self, request):
        path = request.path_info.rstrip("/") or "/"

        return (
            request.method in {"GET", "HEAD"}
            and not self._is_excluded_path(path)
            and not self._has_locale_prefix(path)
        )

    def _is_excluded_path(self, path):
        return any(path == prefix or path.startswith(f"{prefix}/") for prefix in self.excluded_prefixes)

    @classmethod
    def _has_locale_prefix(cls, path):
        first_segment = path.strip("/").split("/", 1)[0].casefold()

        supported_locales = {language_code.casefold() for language_code, _ in settings.LANGUAGES}
        supported_locales.update(alias.casefold() for alias in cls.locale_aliases)

        return first_segment in supported_locales

    @staticmethod
    def _get_preferred_language(request):
        language_code = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        if not language_code:
            return None

        try:
            # Get the supported language variant to ensure it matches one of the configured languages
            language_code = trans_real.get_supported_language_variant(language_code)
        except LookupError:
            return None

        # Check if the language code corresponds to a valid Locale in the database
        if not Locale.objects.filter(language_code=language_code).exists():
            return None

        return language_code
