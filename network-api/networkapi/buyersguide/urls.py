from django.conf.urls import url
from networkapi.buyersguide import views


urlpatterns = [
    url(r'^$', views.buyersguide_home, name='buyersguide-home'),
    url(r'^about/', views.about_view, name='about-view'),
    url(r'^product/(?P<productname>[\w\ ]+)/', views.product_view, name='product-view'),
]
