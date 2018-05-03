from django.conf.urls import url
from networkapi.fellows import views
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', views.fellows_home, name='fellowships-home'),
    url(r'^directory/$',
        views.fellows_directory,
        name='fellowships-directory'),
    url(r'^support/$', views.fellows_support, name='fellowships-support'),
    url(r'^get-involved/$', views.fellows_get_involved, name='fellowships-get-involved'),
    url(r'^(?P<program_type_slug>[-\w]+)/$',
        views.fellows_type,
        name='fellowships-type'),
]
