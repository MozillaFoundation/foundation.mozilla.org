from django import template
from ..utils import get_menu_pages

register = template.Library()


# Instantiate a primary page top nav menu based on the current page's relation to other pages
@register.inclusion_tag('wagtailpages/tags/primary_page_menu.html', takes_context=True)
def primary_page_menu(context, page):
    # Return the list of values we need to have our template
    # generate the appropriate sidebar HTML.
    return {
        'singleton_page': context['singleton_page'],
        'current': page,
        'menu_pages': get_menu_pages(context['root']),
    }
