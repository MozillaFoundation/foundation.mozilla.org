from django.urls import re_path

from networkapi.milestones.views import (
    MilestoneListView,
    MilestoneView,
)

urlpatterns = [
    re_path('^$', MilestoneListView.as_view(), name='milestone-list'),
    re_path(r'^(?P<pk>[0-9]+)/', MilestoneView.as_view(), name='milestone'),
]
