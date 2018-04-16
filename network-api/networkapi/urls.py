'''networkapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
'''
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from wagtail.admin import urls as wagtailadmin_urls
# from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from networkapi.views import EnvVariablesView

admin.autodiscover()

urlpatterns = list(filter(None, [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fellowships/', include('networkapi.fellows.urls')),

    # Wagtail CMS routes for admin
    url(r'^cms/', include(wagtailadmin_urls)),

    # We don't use Wagtail documents at the moment.
    # url(r'^documents/', include(wagtaildocs_urls)),

    # Wagtail CMS 'live' namespace, used for pages that are
    # at present still served using mezzanine (opportunities
    # and campaigns as of this change).
    url(r'^wagtail/', include(wagtail_urls)),

    # super special url for documentation purposes
    url(
        r'^how-do-i-wagtail/',
        RedirectView.as_view(url='/wagtail/docs/how-do-i-wagtail/'),
        name='how-do-i-wagtail'
    ),

    url(r'^fellowship/(?P<path>.*)', RedirectView.as_view(
        url='/fellowships/%(path)s',
        query_string=True
    )),

    url(r'^fellowships/directory/archive', RedirectView.as_view(
        url='/fellowships/directory',
        query_string=True
    )),

    url(r'^soc/', include('social_django.urls', namespace='social')),

    # network-api routes:
    url(r'^api/people/', include('networkapi.people.urls')),
    url(r'^api/news/', include('networkapi.news.urls')),
    url(r'^api/milestones/', include('networkapi.milestones.urls')),
    url(r'^api/highlights/', include('networkapi.highlights.urls')),
    url(r'^api/homepage/', include('networkapi.homepage.urls')),
    url(r'^api/campaign/', include('networkapi.campaign.urls')),
    url(r'^environment.json', EnvVariablesView.as_view()),

    # Wagtail CMS live routes
    url(r'^(?!opportunity|campaigns)', include(wagtail_urls)),

    # Wagtail homepage
    url(r'^$', RedirectView.as_view(
        url='/wagtail',
        query_string=True
    ), {'slug': '/'}, name='home'),

    # Fallback Mezzanine routes, only still used for
    # opportunities and campaigns as of this change.
    url(r'^', include('mezzanine.urls')),
]))


handler404 = RedirectView.as_view(url='/errors/404')
handler500 = 'mezzanine.core.views.server_error'

if settings.USE_S3 is not True:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
