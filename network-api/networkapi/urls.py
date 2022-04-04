from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, re_path, include
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.i18n import set_language, JavaScriptCatalog

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

# The following line is commented off in favour of the utility import,
# to allow better URL matching by wagtail (which, by default only
# matches on slug-compliant URLs).
#
# See https://github.com/mozilla/foundation.mozilla.org/issues/6464

# from wagtail.core import urls as wagtail_urls
from .utility import watail_core_url_override as wagtail_urls
from .sitemaps import sitemap

from wagtail_footnotes import urls as footnotes_urls
from networkapi.wagtailcustomization.image_url_tag_urls import urlpatterns as image_url_tag_urls
from networkapi.views import EnvVariablesView, review_app_help_view
from networkapi.wagtailpages.rss import RSSFeed, AtomFeed
from networkapi.redirects import foundation_redirects

admin.autodiscover()


def get_robots_content():
    """
    Do not allow indexing of any content, except on the live site.
    """
    if settings.ASSET_DOMAIN != 'foundation.mozilla.org':
        return """
User-Agent: *
Disallow: /
        """.strip()

    # For anti-spam purposes, explicitly disallow indexing the thimble artifact page.
    return """
User-Agent: *
Disallow: /*/artifacts/thimble
Disallow: /artifacts/thimble
crawl-delay: 10
""".strip()


def csrf_response(request):
    response = render(request, 'api/csrf.html')
    response['Cache-Control'] = 'no-cache'
    return response


urlpatterns = list(filter(None, [
    path('robots.txt', lambda x: HttpResponse(
        get_robots_content(),
        content_type='text/plain; charset=utf-8'),
        name='robots_file'
        ),

    # Google verification
    path('googled2a9d510ca850787.html', lambda x: HttpResponse(
        'google-site-verification: googled2a9d510ca850787.html',
        content_type='text/html; charset=utf-8'),
        name='googled2a9d510ca850787.html'
        ),

    # social-sign-on routes so that Google auth works
    re_path(r'^soc/', include('social_django.urls', namespace='social')),

    # CSRF endpoint
    re_path(r'^api/csrf/', csrf_response),

    # network API routes:

    re_path(r'^api/campaign/', include('networkapi.campaign.urls')),
    re_path(r'^api/highlights/', include('networkapi.highlights.urls')),
    re_path(r'^api/news/', include('networkapi.news.urls')),
    re_path(r'^api/people/', include('networkapi.people.urls')),
    re_path(r'^environment.json', EnvVariablesView.as_view()),
    re_path(r'^help/', review_app_help_view, name='Review app help'),
    re_path(r'^tito/', include('networkapi.events.urls')),

    # Wagtail CMS routes
    re_path(
        r'^how-do-i-wagtail/',
        RedirectView.as_view(url='/docs/how-do-i-wagtail/'),
        name='how-do-i-wagtail'
    ),
    path('', include(image_url_tag_urls)),

    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^en/cms/', RedirectView.as_view(url='/cms/')),
    re_path(r'^documents/', include(wagtaildocs_urls)),

    # This shims sentry's reporting URL, so that when you're running with
    # sentry enabled locally, rather than sending sentry errors over to the
    # remote service (which is guaranteed to reject the data), we generate
    # an intentional exception so that python writes an error to the console
    # locally, with a traceback. The role of sentry is to surface errors that
    # happen in the user's browser, which we can normally not look at without
    # sending over to a logging service, but when doing local dev we can see
    # browser errors just fine.
    path('sentry-debug', lambda r:  1 / 0) if settings.SENTRY_DSN and settings.DEBUG else None,

    # set up set language redirect view
    path('i18n/setlang/', csrf_exempt(set_language), name='set_language'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),

    # Wagtail Footnotes package
    path("footnotes/", include(footnotes_urls)),

    # redirect /pt to /pt-BR. See https://github.com/mozilla/foundation.mozilla.org/issues/5993
    re_path(r'^pt/(?P<rest>.*)', RedirectView.as_view(url='/pt-BR/%(rest)s', query_string=True, permanent=True)),
]))

# Anything that needs to respect the localised
# url format with /<language_code>/ infixed needs
# to be wrapped by django's i18n_patterns feature:
urlpatterns += i18n_patterns(
    # Blog RSS feed
    path('blog/rss/', RSSFeed(), name='rss-feed'),
    path('blog/atom/', AtomFeed()),

    # Redirects
    *foundation_redirects(),

    # wagtail-managed data
    re_path(r'', include(wagtail_urls)),

    path('sitemap.xml', cache_page(86400)(sitemap)),
)

if settings.USE_S3 is not True:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

if settings.DEBUG:
    urlpatterns += (
        path('maintenance/', TemplateView.as_view(template_name="maintenance/maintenance.html")),
    )

# Use a custom 404 handler so that we can serve distinct 404
# pages for each "site" that wagtail services.
handler404 = 'networkapi.wagtailpages.views.custom404_view'

# Use a custom 500 handler if and only if Django refuses to give any stack
# traces for server error 500... And even then, do not use this on prod.
if settings.FORCE_500_STACK_TRACES is True:
    handler500 = 'networkapi.utility.custom_url_handlers.server_error_500_handler'
