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
from django.conf.urls.static import static

import mezzanine
from mezzanine.conf import settings

admin.autodiscover()

urlpatterns = list(filter(None, [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^soc/', include('social_django.urls', namespace='social'))
    if settings.SOCIAL_SIGNIN else '',
    # network-api routes:
    url(r'^api/people/', include('networkapi.people.urls')),
    url(r'^api/news/', include('networkapi.news.urls')),
    url(r'^api/highlights/', include('networkapi.highlights.urls')),
    url(r'^$', mezzanine.pages.views.page, {'slug': '/'}, name='home'),
    url(r'^', include('mezzanine.urls')),
]))


# handler404 = RedirectView.as_view(url='/errors/404')
handler404 = 'mezzanine.core.views.page_not_found'
handler500 = 'mezzanine.core.views.server_error'

if settings.USE_S3 is not True:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
