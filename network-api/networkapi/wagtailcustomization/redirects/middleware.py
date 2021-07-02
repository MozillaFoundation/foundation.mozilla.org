from wagtail.contrib.redirects import middleware

# We want to wrap the _get_redirect logic, so we need to cache the original.
_original_get_redirect = middleware._get_redirect


# Then we can create a wrapper around the original logic:
def _new_get_redirect(request, path):
    if hasattr(request, 'LANGUAGE_CODE'):
        # If this path has an i18n_patterns locale prefix, remove it.
        locale_prefix = f'/{request.LANGUAGE_CODE}/'
        if path.startswith(locale_prefix):
            path = path.replace(locale_prefix, '/', 1)
    if 'QUERY_STRING' in request.META:
        query_string = request.META['QUERY_STRING']
        path = path + f'/{query_string}'
    # Then hand off processing to the original redirect logic.
    return _original_get_redirect(request, path)


# Then shim the redirect middleware...
middleware._get_redirect = _new_get_redirect


# ...and re-export without anything else any the wiser.
RedirectMiddleware = middleware.RedirectMiddleware
