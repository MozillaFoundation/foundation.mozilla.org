from django import template
from django.apps import apps
from urllib.parse import urlparse

register = template.Library()


# Returns the PNI home page
@register.simple_tag(name='get_bg_home_page')
def get_bg_home_page():
    BuyersGuidePage = apps.get_model(app_label='wagtailpages', model_name='BuyersGuidePage')
    pni_home_page = BuyersGuidePage.objects.first()
    return pni_home_page


# Determine if a category nav link should be marked active
@register.simple_tag(name='check_active_category')
def check_active_category(current_category, target_category):
    # because we're working with potentially localized data,
    # make sure to compare the linguistic originals.
    current_category = getattr(current_category, 'original', current_category)
    target_category = getattr(target_category, 'original', target_category)
    match = current_category == target_category
    if hasattr(current_category, 'parent'):
        match = match or current_category.parent == target_category
    return 'active' if match else ''


# Determine if a nav link should be active.
@register.simple_tag(name='bg_active_nav')
def bg_active_nav(current, target):
    return 'active' if urlparse(current).path == urlparse(target).path else ''


@register.simple_tag(name='product_in_category')
def product_in_category(productpage, categorySlug):
    if categorySlug == "":
        return True
    categories = productpage.product_categories.all()
    return categorySlug in [cat.category.slug for cat in categories]
