from django.conf.urls import url
from networkapi.fellows import views

urlpatterns = [
    url(r'^$', views.fellows_home),
    url(r'^directory/$', views.fellows_directory),
    url(r'^support/$', views.fellows_support),
    url(r'^apply/$', views.fellows_apply),
]
