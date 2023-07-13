from django.urls import re_path

from networkapi.campaign.views import signup_submission_view

urlpatterns = [
    re_path(r"^signups/(?P<pk>[0-9]+)/", signup_submission_view, name="signup-submission"),
]
