from django.urls import re_path

from networkapi.buyersguide import views

urlpatterns = [
    # re_path(r'^$', views.buyersguide_home, name='buyersguide-home'),
    # re_path(r'^contest', views.contest_view, name='contest-view'),
    # re_path(r'^about/press', views.bg_about_page("press"), name='press-view'),
    # re_path(r'^about/contact', views.bg_about_page("contact"), name='contact-view'),
    # re_path(r'^about/methodology', views.bg_about_page("methodology"), name='methodology-view'),
    # re_path(
    #     r'^about/meets-minimum-security-standards',
    #     views.bg_about_page("minimum_security"),
    #     name='min-security-view'
    # ),
    # re_path(r'^about/why', views.bg_about_page("why_we_made"), name='about-why-view'),
    # re_path(r'^about/', views.bg_about_page("how_to_use"), name='how-to-use-view'),
    # re_path(r'^categories/(?P<slug>[\w\W]+)/', views.category_view, name='category-view'),
    # re_path(r'^products/(?P<slug>[-\w\d]+)/$', views.product_view, name='product-view'),
]
