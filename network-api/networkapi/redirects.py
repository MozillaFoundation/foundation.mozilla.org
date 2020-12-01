from django.urls import re_path

from networkapi.wagtailpages.views import localized_redirect


def foundation_redirects():
    return [
        # redirect /opportunity Wagtail pages to /initiatives
        # see https://github.com/mozilla/foundation.mozilla.org/issues/2971 for context
        re_path(
            r'^opportunity/(?P<subpath>.*)',
            lambda req, subpath: localized_redirect(req, subpath, 'initiatives')
        ),

        # redirect /about Wagtail pages to /who-we-are
        re_path(
            r'^about/(?P<subpath>.*)',
            lambda req, subpath: localized_redirect(req, subpath, 'who-we-are')
        ),

        # redirect /participate Wagtail pages to /what-you-can-do
        re_path(
            r'^participate/(?P<subpath>.*)',
            lambda req, subpath: localized_redirect(req, subpath, 'what-you-can-do')
        ),
    ]
