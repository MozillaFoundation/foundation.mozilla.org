from django.conf.urls import url

from networkapi.buyersguide import views

urlpatterns = [
    url(r'^$', views.buyersguide_home, name='buyersguide-home'),
    url(r'^about/why', views.why_view, name='why-view'),
    url(r'^about/', views.about_view, name='about-view'),
    url(r'^categories/(?P<slug>[\w\W]+)/', views.category_view, name='category-view'),
    url(r'^products/(?P<slug>[-\w\d]+)/$', views.product_view, name='product-view'),
]
