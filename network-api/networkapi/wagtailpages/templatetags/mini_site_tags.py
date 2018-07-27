from django import template
from ..utils import get_mini_side_nav_data

register = template.Library()


# Instantiate a mini-site sidebar menu based on the current page's relation to other pages
@register.inclusion_tag('wagtailpages/tags/mini_site_sidebar.html', takes_context=True)
def mini_site_sidebar(context, page):
    return get_mini_side_nav_data(context, page)


# Instantiate a mini-site horizontal nav based on the current page's relation to other pages
@register.inclusion_tag('wagtailpages/tags/mini_site_horizontal_nav.html', takes_context=True)
def mini_site_horizontal_nav(context, page):
    return get_mini_side_nav_data(context, page)


# Render a page's CTA (petition, signup, etc.)
@register.inclusion_tag('wagtailpages/tags/cta.html', takes_context=True)
def cta(context, page):
    cta = page.cta
    return {
        'cta': cta,
        'modals_json': page.get_donation_modal_json(),
        'cta_type': cta.__class__.__name__,
    }
