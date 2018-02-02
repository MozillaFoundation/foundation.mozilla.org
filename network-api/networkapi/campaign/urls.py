from django.conf.urls import url

from networkapi.campaign.views import petition_submission_view

urlpatterns = [
    url(r'^petitions/(?P<pk>[0-9]+)/', petition_submission_view, name='petition-submission'),
]
