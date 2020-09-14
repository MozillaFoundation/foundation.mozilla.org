from django.conf.urls import url

from networkapi.wagtailpages.views import localized_redirect


def foundation_redirects():
    return [
        # redirect /opportunity Wagtail pages to /initiatives
        # see https://github.com/mozilla/foundation.mozilla.org/issues/2971 for context
        url(r'^opportunity/(?P<subpath>.*)', lambda req, subpath: localized_redirect(req, subpath, 'initiatives')),

        # redirect /about Wagtail pages to /who-we-are
        url(r'^about/(?P<subpath>.*)', lambda req, subpath: localized_redirect(req, subpath, 'who-we-are')),

        # redirect /participate Wagtail pages to /what-you-can-do
        url(r'^participate/(?P<subpath>.*)', lambda req, subpath: localized_redirect(req, subpath, 'what-you-can-do')),
    ]
