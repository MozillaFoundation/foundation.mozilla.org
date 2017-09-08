from django.conf.urls import url

from networkapi.homepage.views import HomepageView

urlpatterns = [
    url('^$', HomepageView.as_view(), name='homepage'),
]
