from django.conf.urls import url

from networkapi.buyersguide import views

urlpatterns = [
    url(r'^$', views.buyersguide_home, name='buyersguide-home'),
    url(r'^about/press', views.bg_about_page("press"), name='press-view'),
    url(r'^about/contact', views.bg_about_page("contact"), name='contact-view'),
    url(r'^about/methodology', views.bg_about_page("methodology"), name='methodology-view'),
    url(r'^about/meets-minimum-security-standards', views.bg_about_page("minimum_security"), name='min-security-view'),
    url(r'^about/why', views.bg_about_page("why_we_made"), name='why-view'),
    url(r'^about/', views.bg_about_page("how_to_use"), name='how-to-use-view'),
    url(r'^categories/(?P<slug>[\w\W]+)/', views.category_view, name='category-view'),
    url(r'^products/(?P<slug>[-\w\d]+)/$', views.product_view, name='product-view'),
]
