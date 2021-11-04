from django import template
from urllib.parse import urlparse

register = template.Library()


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


@register.simple_tag(name='prod_in_cat')
def prod_in_cat(productpage, categorySlug):
    if categorySlug == "":
        return True
    return categorySlug in [cat.category.slug for cat in productpage.product_categories.all()]


"""
# Instantiate a list of category page links based on the current page's relation to them
# NOTE: this points to the new, namespaced category_nav_links. If we need to revert to the old app, change this back.
@register.inclusion_tag('buyersguide/fragments/category_nav_links.html', takes_context=True)
def category_nav(context, current_url, current_category, all_categories):
    return {
        'current_url': current_url,
        'current_category': current_category,
        'sorted_categories': all_categories.order_by('-featured', 'sort_order', 'name'),  # featured categories first
    }
"""
