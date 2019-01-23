from django import template
from ..utils import get_mini_side_nav_data

register = template.Library()


# Instantiate a horizontal nav based on the current page's relation to other pages
@register.inclusion_tag('wagtailpages/tags/horizontal_nav.html', takes_context=True)
def horizontal_nav(context, current_page, menu_pages, classname=""):
    # return get_mini_side_nav_data(context, page)
    return {
        'current': current_page,
        'menu_pages': menu_pages,
        'classname': classname,
    }

