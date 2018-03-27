from django import template

register = template.Library()


# Instantiate a mini-site sidebar menu based on the current page's relation to other pages
@register.inclusion_tag('wagtailpages/tags/mini_site_sidebar.html', takes_context=True)
def mini_site_sidebar(context, page):
    children = page.get_children().live()

    root = context['root']
    if page is not root:
        children = root.get_children().live()

    menu_pages = [root] + list(children.in_menu())

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
