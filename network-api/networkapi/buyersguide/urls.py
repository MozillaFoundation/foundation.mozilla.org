from django.conf.urls import url
from django.http import HttpResponseRedirect

from networkapi.buyersguide import views

def undo_locale_code(request, path):
    """
    Redirect to the base Buyers Guide URL
    """
    return HttpResponseRedirect(f"/privacynotincluded/{path}")

# This will remove any locale code prefix for the Buyers Guide
remove_locale_for_buyers_guide = url(r'^(\w\w(-\W\W)?)/privacynotincluded/(?P<path>[\w\W]*)$', undo_locale_code)

urlpatterns = [
    url(r'^$', views.buyersguide_home, name='buyersguide-home'),
    url(r'^about/', views.about_view, name='about-view'),
    url(r'^categories/(?P<categoryname>[\w\W]+)/', views.category_view, name='category-view'),
    url(r'^products/(?P<slug>[-\w]+)/$', views.product_view, name='product-view'),
    url(r'^vote$', views.product_vote, name='product-vote'),
]
