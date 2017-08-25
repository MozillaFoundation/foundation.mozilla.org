from django.conf.urls import url

from networkapi.milestones.views import (
    MilestoneListView,
    MilestoneView,
)

urlpatterns = [
    url('^$', MilestoneListView.as_view(), name='milestone-list'),
    url(r'^(?P<pk>[0-9]+)/', MilestoneView.as_view(), name='milestone'),
]
