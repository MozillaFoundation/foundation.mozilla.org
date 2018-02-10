from django.conf.urls import url
from networkapi.fellows import views

urlpatterns = [
    url(r'^$', views.fellows_home, name='fellowships-home'),
    url(r'^science/$', views.fellows_science, name='fellowships-science'),
    url(r'^open-web/$', views.fellows_openweb, name='fellowships-open-web'),
    url(r'^directory/$',
        views.fellows_directory,
        name='fellowships-directory'),
    url(r'^directory/(?P<program_type_slug>[-\w]+)/$',
        views.fellows_directoy_type,
        name='fellowships-directory-senior'),
    url(r'^support/$', views.fellows_support, name='fellowships-support'),
    url(r'^apply/$', views.fellows_apply, name='fellowships-apply'),
]
