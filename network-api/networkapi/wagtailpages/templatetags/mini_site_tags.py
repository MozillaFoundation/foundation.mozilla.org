from django import template

register = template.Library()


def get_descendants(node, list, depth=0, max_depth=2):
    if (depth <= max_depth):
        list.append({
            'page': node,
            'depth': depth,
        })
        for child in node.get_children().live().in_menu():
            get_descendants(child, list, depth + 1)


# Instantiate a mini-site sidebar menu based on the current page's relation to other pages
@register.inclusion_tag('wagtailpages/tags/mini_site_sidebar.html', takes_context=True)
def mini_site_sidebar(context, page):
    menu_pages = list()
    root = context['root']
    get_descendants(root, menu_pages)

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
