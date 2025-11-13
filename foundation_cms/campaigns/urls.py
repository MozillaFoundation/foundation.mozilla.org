from django.urls import path

from . import views

app_name = "campaigns"

urlpatterns = [
    path("petition/submit/", views.petition_submit, name="petition_submit"),
]
