from django.urls import path, re_path

from networkapi.news.views import NewsListView, NewsView

urlpatterns = [
    path("", NewsListView.as_view(), name="news-list"),
    re_path(r"^(?P<pk>[0-9]+)/", NewsView.as_view(), name="news"),
]
