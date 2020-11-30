from django.apps import AppConfig
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

from wagtail.core import hooks


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/admin.css to the admin."""
    return format_html('<link rel="stylesheet" href="{}">', static("css/admin.css"))


class UnlocalizeRedirectsConfig(AppConfig):
    """
    Patch the _get_redirect function such that it removes locale prefixes
    before actual redirect testing happens, as we use wagtail-modeltranslations,
    and there is no such thing as "redirect only page(s) from locale(s) X, ..., Z"
    """

    def ready(self):
        from wagtail.contrib.redirects import middleware as redirect_middleware

        # We want to wrap the _get_redirect logic, so we need to cache the original.
        _original_get_redirect = redirect_middleware._get_redirect

        def _new_get_redirect(request, path):
            # If this path has an i18n_patterns locale prefix, remove it.
            if hasattr(request, 'LANGUAGE_CODE'):
                localePrefix = f'{request.LANGUAGE_CODE}/'
                if path.startswith(localePrefix):
                    path = path.replace(localePrefix, '', 1)

            # Then hand off processing to the original redirect logic.
            _original_get_redirect(request, path)

        redirect_middleware._get_redirect = _new_get_redirect
