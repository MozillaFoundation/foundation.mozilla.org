from django.conf.urls import url

from networkapi.news.views import (
    NewsListView,
    NewsView,
)

urlpatterns = [
    url('^$', NewsListView.as_view(), name='news-list'),
    url(r'^(?P<pk>[0-9]+)/', NewsView.as_view(), name='news'),
]
