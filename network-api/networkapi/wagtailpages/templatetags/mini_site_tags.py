from django import template
from django.core.exceptions import ObjectDoesNotExist
from ..utils import get_mini_side_nav_data
from networkapi.wagtailpages.models import CTA


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
    cta = {
        'page': page,
        'cta': None,
        'cta_type': None
    }

    if page.cta:
        for (Subclass, subclass_name) in [(sub, sub.__name__.lower(),) for sub in CTA.__subclasses__()]:
            try:
                cta['cta'] = Subclass.objects.get(pk=page.cta.pk)
                cta['cta_type'] = subclass_name
                break
            except ObjectDoesNotExist:
                pass

    # Only campaign pages currently have donation modal CTA data
    # associated with them, so only add this if the accessor
    # for it exists for the page type we're rendering.
    if hasattr(page, 'get_donation_modal_json'):
        cta['modals_json'] = page.get_donation_modal_json()

    return cta
