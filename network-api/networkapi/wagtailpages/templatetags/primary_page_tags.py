from django import template
from ..utils import get_mini_side_nav_data

register = template.Library()


# Instantiate a primary page top nav menu based on the current page's relation to other pages
@register.inclusion_tag('wagtailpages/tags/primary_page_menu.html', takes_context=True)
def primary_page_menu(context, page):
    return get_mini_side_nav_data(context, page, no_minimum_page_count=True)
