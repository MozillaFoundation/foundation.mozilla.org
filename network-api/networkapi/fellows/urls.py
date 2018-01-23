from django.conf.urls import url
from networkapi.fellows import views

urlpatterns = [
    url(r'^$', views.fellows_home, name='fellowships-home'),
    url(r'^directory/$', views.fellows_directory, name='fellowships-directory'),
    url(r'^support/$', views.fellows_support, name='fellowships-support'),
    url(r'^science/$', views.fellows_science, name='fellowships-science'),
    url(r'^open-web/$', views.fellows_openweb, name='fellowships-open-web'),
]
