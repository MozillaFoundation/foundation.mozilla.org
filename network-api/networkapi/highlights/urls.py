from django.conf.urls import url

from networkapi.highlights.views import (
    HighlightListView,
    HighlightView,
)

urlpatterns = [
    url('^$', HighlightListView.as_view(), name='highlight-list'),
    url(r'^(?P<pk>[0-9]+)/', HighlightView.as_view(), name='highlight'),
]
