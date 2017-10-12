from django.conf.urls import url

from networkapi.people.views import (
    PeopleListView,
    PersonView,
)

urlpatterns = [
    url('^$', PeopleListView.as_view(), name='people-list'),
    url(r'^(?P<pk>[0-9]+)/', PersonView.as_view(), name='person'),
]
