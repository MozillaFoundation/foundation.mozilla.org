from django.conf import settings
from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.i18n import set_language

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

# The following line is commented off in favour of the utility import,
# to allow better URL matching by wagtail (which, by default only
# matches on slug-compliant URLs).
#
# See https://github.com/mozilla/foundation.mozilla.org/issues/6464

# from wagtail.core import urls as wagtail_urls
from .utility import watail_core_url_override as wagtail_urls

from wagtail.contrib.sitemaps.views import sitemap
from wagtail_footnotes import urls as footnotes_urls
from networkapi.wagtailcustomization.image_url_tag_urls import urlpatterns as image_url_tag_urls
from networkapi.views import EnvVariablesView, review_app_help_view
from networkapi.wagtailpages.rss import RSSFeed, AtomFeed
from networkapi.redirects import foundation_redirects
from experiments import views as experiment_views
admin.autodiscover()

urlpatterns = list(filter(None, [
    # Add robots.txt to exclude the thimble artifact page
    path('robots.txt', lambda x: HttpResponse(
        "User-Agent: *\nDisallow: /*artifacts/thimble",
        content_type="text/plain; charset=utf-8"),
         name="robots_file"
         ),

    # social-sign-on routes so that Google auth works
    re_path(r'^soc/', include('social_django.urls', namespace='social')),

    # network API routes:

    re_path(r'^api/campaign/', include('networkapi.campaign.urls')),
    re_path(r'^api/highlights/', include('networkapi.highlights.urls')),
    re_path(r'^api/news/', include('networkapi.news.urls')),
    re_path(r'^api/people/', include('networkapi.people.urls')),
    re_path(r'^api/experiments/complete/([^\/]+)/$', experiment_views.record_completion),
    re_path(r'^environment.json', EnvVariablesView.as_view()),
    re_path(r'^help/', review_app_help_view, name='Review app help'),

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
    re_path(r'^sitemap.xml$', sitemap),

    # Sentry test url
    path('sentry-debug', lambda r:  1 / 0) if settings.SENTRY_DSN and settings.DEBUG else None,

    # set up set language redirect view
    path('i18n/setlang/', csrf_exempt(set_language), name='set_language'),

    # Wagtail Footnotes package
    path("footnotes/", include(footnotes_urls)),
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
