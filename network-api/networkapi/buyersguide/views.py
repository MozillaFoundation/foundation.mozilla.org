import re
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import Error
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes, throttle_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser

from networkapi.buyersguide.models import Product, BuyersGuideProductCategory, BooleanVote, RangeVote
from networkapi.buyersguide.throttle import UserVoteRateThrottle, TestUserVoteRateThrottle

vote_throttle_class = UserVoteRateThrottle if not settings.TESTING else TestUserVoteRateThrottle

path_regex = re.compile(r"^/\w\w/")


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
    return re.sub(path_regex, '/en/', path, count=1)


def buyersguide_home(request):
    if not path_is_en_prefixed(request.path):
        return redirect(get_en_redirect(request.path), permanent=False)

    products = cache.get('sorted_product_dicts')

    if not products:
        products = [p.to_dict() for p in Product.objects.all()]
        products.sort(key=lambda p: get_average_creepiness(p))
        cache.set('sorted_product_dicts', products, 86400)

    return render(request, 'buyersguide_home.html', {
        'categories': BuyersGuideProductCategory.objects.all(),
        'products': products,
        'mediaUrl': settings.MEDIA_URL,
    })


def category_view(request, categoryname):
    if not path_is_en_prefixed(request.path):
        return redirect(get_en_redirect(request.path), permanent=False)

    category = get_object_or_404(BuyersGuideProductCategory, name__iexact=categoryname)
    products = [p.to_dict() for p in Product.objects.filter(product_category__in=[category]).distinct()]
    return render(request, 'category_page.html', {
        'categories': BuyersGuideProductCategory.objects.all(),
        'category': category,
        'products': products,
        'mediaUrl': settings.MEDIA_URL,
    })


def product_view(request, slug):
    if not path_is_en_prefixed(request.path):
        return redirect(get_en_redirect(request.path), permanent=False)

    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_page.html', {
        'categories': BuyersGuideProductCategory.objects.all(),
        'product': product.to_dict(),
        'mediaUrl': settings.MEDIA_URL,
        'coralTalkServerUrl': settings.CORAL_TALK_SERVER_URL,
    })


def about_view(request):
    if not path_is_en_prefixed(request.path):
        return redirect(get_en_redirect(request.path), permanent=False)

    return render(request, 'about.html', {
        'categories': BuyersGuideProductCategory.objects.all(),
    })


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
def refresh_cache(request):
    products = [p.to_dict() for p in Product.objects.all()]
    products.sort(key=lambda p: get_average_creepiness(p))
    cache.set('sorted_product_dicts', products, 86400)
    return redirect('/cms/buyersguide/product/')
