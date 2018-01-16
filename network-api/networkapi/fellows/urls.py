from django.conf.urls import url
from networkapi.fellows import views

urlpatterns = [
    url('', views.fellows_home),
]
