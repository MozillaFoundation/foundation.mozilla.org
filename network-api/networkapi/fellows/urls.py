from django.conf.urls import url
from networkapi.fellows import views

urlpatterns = [
    url(r'^$', views.fellows_home, name='fellowships-home'),
    url(r'^science/$', views.fellows_science, name='fellowships-science'),
    url(r'^open-web/$', views.fellows_openweb, name='fellowships-open-web'),
    url(r'^tech-policy/$', views.fellows_tech_policy, name='fellowships-tech-policy'),
    url(r'^media/$', views.fellows_media, name='fellowships-media'),
    url(r'^directory/$',
        views.fellows_directory,
        name='fellowships-directory'),
    url(r'^directory/(?P<program_type_slug>[-\w]+)/$',
        views.fellows_directoy_type,
        name='fellowships-directory-type'),
    url(r'^support/$', views.fellows_support, name='fellowships-support'),
    url(r'^apply/$', views.fellows_apply, name='fellowships-apply'),
]
