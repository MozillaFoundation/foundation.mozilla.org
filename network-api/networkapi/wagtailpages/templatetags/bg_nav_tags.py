from urllib.parse import urlparse

from django import template
from django.apps import apps
from django.conf import settings

from networkapi.wagtailpages.pagemodels.buyersguide.utils import localize_categories

register = template.Library()


# Finds the page's parent "Buyer's Guide Homepage" and returns it.
@register.simple_tag(name="get_bg_home_page", takes_context=True)
def get_bg_home_page(context):
    BuyersGuidePage = apps.get_model(app_label="wagtailpages", model_name="BuyersGuidePage")
    page = context.get("page", None)
    if page:
        pni_home_page = BuyersGuidePage.objects.ancestor_of(page, inclusive=True).live().first()
    else:
        pni_home_page = BuyersGuidePage.objects.first()
    return pni_home_page


# Determine if a category nav link should be marked active
@register.simple_tag(name="check_active_category")
def check_active_category(current_category, target_category):
    match = current_category == target_category
    if hasattr(current_category, "parent"):
        match = match or current_category.parent == target_category
    return "active" if match else ""


# Determine if a nav (sidebar nav or primary nav) link should be active.
@register.simple_tag(name="bg_active_nav")
def bg_active_nav(current, target, nav="sidebar"):
    if nav == "primary_nav":
        return "active" if urlparse(target).path in urlparse(current).path else ""
    else:
        return "active" if urlparse(target).path == urlparse(current).path else ""


@register.simple_tag(name="product_in_category")
def product_in_category(productpage, categorySlug):
    if categorySlug == "":
        return True
    categories = productpage.product_categories.all()
    return categorySlug in [cat.category.slug for cat in categories]


@register.simple_tag(name="bg_categories_in_subnav")
def bg_categories_in_subnav():
    """Get localised categories that were selected to be in the PNI subnav."""
    default_language = settings.LANGUAGE_CODE
    BuyersGuideCategoryNav = apps.get_model(app_label="wagtailpages", model_name="BuyersGuideCategoryNav")
    BuyersGuideProductCategory = apps.get_model(app_label="wagtailpages", model_name="BuyersGuideProductCategory")

    categories_nav = BuyersGuideCategoryNav.load()
    default_categories = BuyersGuideProductCategory.objects.filter(
        nav_relations__nav=categories_nav, locale__language_code=default_language
    ).order_by("nav_relations__sort_order")

    local_cats = localize_categories(default_categories, preserve_order=True)

    return local_cats


@register.simple_tag(name="bg_non_hidden_categories")
def bg_non_hidden_categories():
    """Get localised categories that were selected to be in the PNI subnav."""
    default_language = settings.LANGUAGE_CODE
    BuyersGuideProductCategory = apps.get_model(app_label="wagtailpages", model_name="BuyersGuideProductCategory")

    default_categories = BuyersGuideProductCategory.objects.filter(
        hidden=False, locale__language_code=default_language
    ).order_by("name")

    all_cats = localize_categories(default_categories, preserve_order=True)

    return all_cats
