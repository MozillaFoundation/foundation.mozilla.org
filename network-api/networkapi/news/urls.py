from django.urls import re_path

from networkapi.news.views import (
    NewsListView,
    NewsView,
)

urlpatterns = [
    re_path('^$', NewsListView.as_view(), name='news-list'),
    re_path(r'^(?P<pk>[0-9]+)/', NewsView.as_view(), name='news'),
]
