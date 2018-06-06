from django import template
from ..utils import get_menu_pages

register = template.Library()


# Instantiate a mini-site sidebar menu based on the current page's relation to other pages
@register.inclusion_tag('wagtailpages/tags/mini_site_sidebar.html', takes_context=True)
def mini_site_sidebar(context, page):
    menu_pages = get_menu_pages(context['root'])

    # We need at least 2 pages, or a nav menu is meaningless.
    if len(menu_pages) < 2:
        menu_pages = False

    # Return the list of values we need to have our template
    # generate the appropriate sidebar HTML.
    return {
        'singleton_page': context['singleton_page'],
        'current': page,
        'menu_pages': menu_pages,
    }


# Instantiate a mini-site horizontal nav based on the current page's relation to other pages
@register.inclusion_tag('wagtailpages/tags/mini_site_horizontal_nav.html', takes_context=True)
def mini_site_horizontal_nav(context, page):
    menu_pages = get_menu_pages(context['root'])

    # We need at least 2 pages, or a nav menu is meaningless.
    if len(menu_pages) < 2:
        menu_pages = False

    # Return the list of values we need to have our template
    # generate the appropriate sidebar HTML.
    return {
        'singleton_page': context['singleton_page'],
        'current': page,
        'menu_pages': menu_pages,
    }


# Render a page's CTA (petition, signup, etc.)
@register.inclusion_tag('wagtailpages/tags/cta.html', takes_context=True)
def cta(context, page):
    cta = page.cta
    return {
        'cta': cta,
        'cta_type': cta.__class__.__name__,
    }
