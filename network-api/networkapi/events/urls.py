from django.urls import re_path

from .views import tito_ticket_completed

urlpatterns = [
    re_path('^ticket-completed/?$', tito_ticket_completed, name='tito-ticket-completed'),
]
