from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from wagtail.contrib.sitemaps.views import sitemap

from networkapi.views import EnvVariablesView, review_app_help_view
from networkapi.buyersguide import views as buyersguide_views

admin.autodiscover()

urlpatterns = list(filter(None, [
    # social-sign-on routes so that Google auth works
    url(r'^soc/', include('social_django.urls', namespace='social')),

    # fellowship routes

    url(r'^fellowships/', include('networkapi.fellows.urls')),

    url(r'^fellowship/(?P<path>.*)', RedirectView.as_view(
        url='/fellowships/%(path)s',
        query_string=True
    )),

    url(r'^fellowships/directory/archive', RedirectView.as_view(
        url='/fellowships/directory',
        query_string=True
    )),

    # network API routes:

    url(r'^api/campaign/', include('networkapi.campaign.urls')),
    url(r'^api/highlights/', include('networkapi.highlights.urls')),
    url(r'^api/news/', include('networkapi.news.urls')),
    url(r'^api/milestones/', include('networkapi.milestones.urls')),
    url(r'^api/people/', include('networkapi.people.urls')),
    url(r'^api/buyersguide/vote/', buyersguide_views.product_vote, name='product-vote'),
    url(r'^api/buyersguide/clear-cache/', buyersguide_views.clear_cache, name='clear-cache'),
    url(r'^environment.json', EnvVariablesView.as_view()),
    url(r'^help/', review_app_help_view, name='Review app help'),

    # Wagtail CMS routes
    url(
        r'^how-do-i-wagtail/',
        RedirectView.as_view(url='/docs/how-do-i-wagtail/'),
        name='how-do-i-wagtail'
    ),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url('^sitemap.xml$', sitemap) if settings.DEBUG else None,
]))

# Anything that needs to respect the localised
# url format with /<language_code>/ infixed needs
# to be wrapped by django's i18n_patterns feature:
urlpatterns += i18n_patterns(
    # Buyer's Guide / Privacy Not Included
    url(r'^privacynotincluded/', include('networkapi.buyersguide.urls')),

    url(r'', include(wagtail_urls)),
)

if settings.USE_S3 is not True:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
