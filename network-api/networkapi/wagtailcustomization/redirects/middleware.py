from urllib.parse import urlencode
from wagtail.contrib.redirects import middleware
from wagtail.contrib.redirects.models import Redirect

# We want to wrap the _get_redirect logic, so we need to cache the original.
_original_get_redirect = middleware._get_redirect


# Then we can create a wrapper around the original logic:
def _new_get_redirect(request, path):
    if hasattr(request, 'LANGUAGE_CODE'):
        # If this path has an i18n_patterns locale prefix, remove it.
        locale_prefix = f'/{request.LANGUAGE_CODE}/'
        if path.startswith(locale_prefix):
            path = path.replace(locale_prefix, '/', 1)

    # Then hand off processing to the original redirect logic.
    redirect = _original_get_redirect(request, path)

    # Wagtail currently does not forward query arguments, so for
    # any URL with stripped query arguments we make a new, on-the-fly
    # redirect with the same path/site bindings, but an updated link
    # with the query arguments restored.
    #
    # See https://github.com/wagtail/wagtail/issues/7339 for more details.
    if redirect and request.GET and "?" not in redirect.link:
        redirect = Redirect(
            old_path=redirect.old_path,
            site=redirect.site,
            redirect_link=f'{redirect.link}?{urlencode(request.GET)}'
        )

    return redirect


# Then shim the redirect middleware...
middleware._get_redirect = _new_get_redirect


# ...and re-export without anything else any the wiser.
RedirectMiddleware = middleware.RedirectMiddleware
