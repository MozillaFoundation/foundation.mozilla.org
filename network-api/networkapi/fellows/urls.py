from django.conf.urls import url

from networkapi.fellows import views
from networkapi.fellows.views import (
    FellowHomeView,
    FellowDirectoryView,
    FellowSupportView,
    FellowScienceView,
    FellowOpenWebView,
)

urlpatterns = [
    url(r'^$', FellowHomeView.as_view(), name='fellowships-home'),
    url(r'^directory/$', FellowDirectoryView.as_view(), name='fellowships-directory'),
    url(r'^support/$', FellowSupportView.as_view(), name='fellowships-support'),
    url(r'^science/$', FellowScienceView.as_view(), name='fellowships-science'),
    url(r'^open-web/$', FellowOpenWebView.as_view(), name='fellowships-open-web'),
]
