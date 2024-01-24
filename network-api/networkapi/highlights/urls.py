from django.urls import path, re_path

from networkapi.highlights.views import HighlightListView, HighlightView

urlpatterns = [
    path("", HighlightListView.as_view(), name="highlight-list"),
    re_path(r"^(?P<pk>[0-9]+)/", HighlightView.as_view(), name="highlight"),
]
