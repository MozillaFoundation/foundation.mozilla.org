from django.conf.urls import url
from networkapi.fellows.views import (
    FellowHomeView,
    FellowDirectoryView,
    FellowSupportView,
    FellowScienceView,
    FellowOpenWebView,
)

urlpatterns = [
    url('^$', FellowHomeView.as_view(), name='fellowships-home'),
    url('^directory/$',
        FellowDirectoryView.as_view(),
        name='fellowships-directory'),
    url('^support/$',
        FellowSupportView.as_view(),
        name='fellowships-support'),
    url('^science/$',
        FellowScienceView.as_view(),
        name='fellowships-science'),
    url('^open-web/$',
        FellowOpenWebView.as_view(),
        name='fellowships-open-web'),
]
