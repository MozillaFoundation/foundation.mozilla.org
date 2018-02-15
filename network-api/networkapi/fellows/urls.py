from django.conf.urls import url
from networkapi.fellows import views

urlpatterns = [
    url(r'^$', views.fellows_home, name='fellowships-home'),
    url(r'^directory/$',
        views.fellows_directory,
        name='fellowships-directory'),
    url(r'^directory/(?P<program_type_slug>[-\w]+)/$',
        views.fellows_directoy_type,
        name='fellowships-directory-type'),
    url(r'^support/$', views.fellows_support, name='fellowships-support'),
    url(r'^apply/$', views.fellows_apply, name='fellowships-apply'),
    url(r'^(?P<program_type_slug>[-\w]+)/$',
        views.fellows_type,
        name='fellowships-type'),
]
