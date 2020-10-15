from django.urls import re_path

from networkapi.people.views import (
    PeopleListView,
    PersonView,
)

urlpatterns = [
    re_path('^$', PeopleListView.as_view(), name='people-list'),
    re_path(r'^(?P<pk>[0-9]+)/', PersonView.as_view(), name='person'),
]
