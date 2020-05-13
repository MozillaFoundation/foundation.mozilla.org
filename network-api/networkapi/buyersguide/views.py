import re

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.conf import settings
from django.db import Error
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404, redirect

from rest_framework.decorators import api_view, parser_classes, throttle_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import (
    Product,
    BooleanVote,
    RangeVote,
    BuyersGuideProductCategory,
)

from .throttle import UserVoteRateThrottle, TestUserVoteRateThrottle
from networkapi.utility.redirects import redirect_to_default_cms_site

vote_throttle_class = UserVoteRateThrottle if not settings.TESTING else TestUserVoteRateThrottle

locale_regex = re.compile(r"^/[a-z]{2}(-[A-Z]{2})?/")


if settings.USE_CLOUDINARY:
    MEDIA_URL = settings.CLOUDINARY_URL
else:
    MEDIA_URL = settings.MEDIA_URL


def get_average_creepiness(product_dict):
    try:
        votes = product_dict['votes']
        creepiness = votes['creepiness']
        avg = creepiness['average']
        return avg

    except TypeError:
        pass

    except AttributeError:
        pass

    return 50


def filter_draft_products(request, products):
    if request.user.is_authenticated:
        return products

    return filter(lambda p: p['draft'] is False, products)


@redirect_to_default_cms_site
def buyersguide_home(request):
    products = cache.get('sorted_product_dicts')

    if not products:
        products = [p.to_dict() for p in Product.objects.all()]
        products.sort(key=lambda p: get_average_creepiness(p))
        cache.set('sorted_product_dicts', products, 86400)

    products = filter_draft_products(request, products)

    return render(request, 'buyersguide_home.html', {
        'categories': BuyersGuideProductCategory.objects.all(),
        'products': products,
        'mediaUrl': MEDIA_URL,
    })


@redirect_to_default_cms_site
def category_view(request, slug):
    key = f'products_category__{slug}'
    products = cache.get(key)

    # If getting by slug fails, also try to get it by name.
    try:
        category = BuyersGuideProductCategory.objects.get(slug=slug)
    except ObjectDoesNotExist:
        category = get_object_or_404(BuyersGuideProductCategory, name__iexact=slug)

    if not products:
        products = [p.to_dict() for p in Product.objects.filter(product_category__in=[category]).distinct()]
        cache.set(key, products, 86400)

    products = filter_draft_products(request, products)

    return render(request, 'category_page.html', {
        'categories': BuyersGuideProductCategory.objects.all(),
        'category': category,
        'products': products,
        'mediaUrl': MEDIA_URL,
    })


@redirect_to_default_cms_site
def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug).specific

    if product.draft and not request.user.is_authenticated:
        raise Http404("Product does not exist")

    product_dict = product.to_dict()
    criteria = [
        'uses_encryption',
        'security_updates',
        'strong_password',
        'manage_vulnerabilities',
        'privacy_policy',
    ]
    total_score = 0
    num_criteria = len(criteria)

    # Calculate the minimum security score
    for i in range(num_criteria):
        value = product_dict[criteria[i]]
        if value == 'Yes':
            total_score += 1
        if value == 'NA':
            total_score += 0.5

    # make sure featured updates come first
    product_dict['updates'] = list(
        product.updates.all().order_by(
            '-featured',
            'pk'
        )
    )

    return render(request, 'product_page.html', {
        'categories': BuyersGuideProductCategory.objects.all(),
        'product': product_dict,
        'mediaUrl': MEDIA_URL,
        'coralTalkServerUrl': settings.CORAL_TALK_SERVER_URL,
        'pageTitle': f'*privacy not included - {product.name}',
        'security_score': total_score,
        'full_security_score': num_criteria
    })


def bg_about_page(template_name):
    @redirect_to_default_cms_site
    def render_view(request):
        key = 'categories'
        categories = cache.get(key)

        if not categories:
            categories = BuyersGuideProductCategory.objects.all()
            cache.set(key, categories, 86400)

        return render(request, f"about/{template_name}.html", {
            'categories': categories,
        })

    return render_view


@api_view(['POST'])
@permission_classes((AllowAny,))
@parser_classes((JSONParser,))
@throttle_classes((vote_throttle_class,))
@csrf_protect
def product_vote(request):
    # Grab the request payload data
    try:
        attribute = request.data['attribute']
        product_id = request.data['productID']
        value = request.data['value']
    except KeyError as ex:
        return Response(f'Missing attribute in payload: {ex}', status=400, content_type='text/plain')

    # validate the data types passed in the request payload
    if not (isinstance(product_id, int) and isinstance(value, (int, bool))):
        return Response('Invalid payload - check data types', status=400, content_type='text/plain')

    try:
        product = Product.objects.get(id=product_id)

        if product.draft and not request.user.is_authenticated:
            raise Http404("Product does not exist")

        VoteClass = RangeVote

        # Check if this vote is a boolean (yes/no) vote, and switch the model if it is
        if isinstance(value, bool):
            VoteClass = BooleanVote

        # Build the model instance
        vote = VoteClass(
            attribute=attribute,
            value=value,
            product=product
        )

        # validate the values are in range (if this is a RangeVote)
        vote.full_clean()

        # persist the vote
        vote.save()

        return Response('Vote recorded', status=201, content_type='text/plain')
    except ObjectDoesNotExist:
        return Response('Invalid product', status=400, content_type='text/plain')
    except ValidationError as ex:
        return Response(f'Payload validation failed: {ex}', status=400, content_type='text/plain')
    except Error as ex:
        print(f'{ex.message} ({type(ex)})')
        return Response('Internal Server Error', status=500, content_type='text/plain')


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def clear_cache(request):
    cache.clear()
    redirect_url = request.POST.get('redirectUrl', '/cms/')
    return redirect(redirect_url)
