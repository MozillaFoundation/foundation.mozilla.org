from django.conf.urls import url
from networkapi.fellows import views

urlpatterns = [
    url(r'^$', views.fellows_home, name='fellowships-home'),
    url(r'^science/$', views.fellows_science, name='fellowships-science'),
    url(r'^open-web/$', views.fellows_openweb, name='fellowships-open-web'),
    url(r'^directory/$',
        views.fellows_directory,
        name='fellowships-directory'),
    url(r'^directory/senior$',
        views.fellows_directory_senior,
        name='fellowships-directory-senior'),
    url(r'^directory/science$',
        views.fellows_directory_science,
        name='fellowships-directory-science'),
    url(r'^directory/open-web$',
        views.fellows_directory_open_web,
        name='fellowships-directory-open-web'),
    url(r'^directory/tech-policy$',
        views.fellows_directory_tech_policy,
        name='fellowships-directory-tech-policy'),
    url(r'^directory/media$',
        views.fellows_directory_senior,
        name='fellowships-directory-media'),
    url(r'^support/$', views.fellows_support, name='fellowships-support'),
    url(r'^apply/$', views.fellows_apply, name='fellowships-apply'),
]
