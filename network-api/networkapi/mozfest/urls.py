from django.urls import re_path

from networkapi.mozfest.views import tito_ticket_completed

urlpatterns = [
    re_path('^ticket-completed/?$', tito_ticket_completed, name='tito-ticket-completed'),
]
