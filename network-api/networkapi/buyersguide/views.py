from django.shortcuts import render
from networkapi.buyersguide.models import Product
from django.contrib.auth.decorators import login_required
from django.conf import settings


# Login required so we can continue to develop this and merge into master without the public seeing it.
# Remove this when we're ready to launch.
@login_required
def buyersguide_home(request):
    products = Product.objects.all()
    return render(request, 'buyersguide_home.html', {'products': products})


@login_required
def product_view(request, productname):
    product = Product.objects.get(name__iexact=productname)
    return render(request, 'product_page.html', {'product': product, 'mediaUrl': settings.MEDIA_URL})


@login_required
def about_view(request):
    return render(request, 'about.html')
