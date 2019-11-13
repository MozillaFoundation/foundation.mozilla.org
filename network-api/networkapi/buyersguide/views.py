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
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from networkapi.buyersguide.models import Product, BuyersGuideProductCategory, BooleanVote, RangeVote
from networkapi.buyersguide.throttle import UserVoteRateThrottle, TestUserVoteRateThrottle

vote_throttle_class = UserVoteRateThrottle if not settings.TESTING else TestUserVoteRateThrottle

locale_regex = re.compile(r"^/[a-z]{2}(-[A-Z]{2})?/")


if settings.USE_CLOUDINARY:
    MEDIA_URL = settings.CLOUDINARY_URL
else:
    MEDIA_URL = settings.MEDIA_URL


def get_average_creepiness(product):
    try:
        votes = product['votes']
        creepiness = votes['creepiness']
        avg = creepiness['average']
        return avg

    except TypeError:
        pass

    return 50


def path_is_en_prefixed(path):
    return path.startswith('/en/')


def get_en_redirect(path):
    redirect_path = re.sub(locale_regex, '/en/', path)
    return redirect(redirect_path, permanent=False)


def enforce_en_locale(view_handler):
    def check_locale(*args, **kwargs):
        path = args[0].path
        if not path_is_en_prefixed(path):
            return get_en_redirect(path)

        return view_handler(*args, **kwargs)

    return check_locale


def filter_draft_products(request, products):
    if request.user.is_authenticated:
        return products

    return filter(lambda p: p['draft'] is False, products)


@enforce_en_locale
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


@enforce_en_locale
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


@enforce_en_locale
def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if product.draft and not request.user.is_authenticated:
        raise Http404("Product does not exist")

    return render(request, 'product_page.html', {
        'categories': BuyersGuideProductCategory.objects.all(),
        'product': product.to_dict(),
        'mediaUrl': MEDIA_URL,
        'coralTalkServerUrl': settings.CORAL_TALK_SERVER_URL,
        'pageTitle': f'*privacy not included - {product.name}',
    })


def bg_about_page(template_name):
    @enforce_en_locale
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
@permission_classes((IsAdminUser,))
def clear_cache(request):
    cache.clear()
    return redirect('/cms/buyersguide/product/')
