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
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from networkapi.views import EnvVariablesView, review_app_help_view

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

    url(r'^api/people/', include('networkapi.people.urls')),
    url(r'^api/news/', include('networkapi.news.urls')),
    url(r'^api/milestones/', include('networkapi.milestones.urls')),
    url(r'^api/highlights/', include('networkapi.highlights.urls')),
    url(r'^api/homepage/', include('networkapi.homepage.urls')),
    url(r'^api/campaign/', include('networkapi.campaign.urls')),
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
    url(r'', include(wagtail_urls)),

    # Mezzanine left-overs

    url(
        # An explicit entry for "a route called 'home'", which we cannot
        # remove until we fully extricate Mezzanine from our codebase:
        r'^this/cannot/be/reached/because/of/the/patterns/above$',
        RedirectView.as_view(url='/its/purely/to/appease/mezzanine'),
        name='home'
    ),
]))


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
