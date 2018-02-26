from django import template

register = template.Library()


# Instantiate a mini-site sidebar menu based on the current page's relation to other pages
@register.inclusion_tag('opportunities/tags/mini_site_sidebar.html', takes_context=True)
def mini_site_sidebar(context, page):

    # do we have children? If so, we're the root page of a mini-site
    children = page.get_children().live()
    has_children = len(children) > 0

    # do we have a parent of the same type that we are?? If we do, two options: either the parent is
    # the same kind of page and we're a child-page in a mini-site, or
    # it's not and we're possibly the root of a mini-site
    ancestors = page.get_ancestors()
    root = next((root for root in ancestors if root.specific_class == page.specific_class), page)
    is_top_page = (root == page)

    # We can now tell whether or not we're part of a mini-site
    singleton = is_top_page and not has_children

    # Grab the necessary level of tree for building the sidebar menu
    if page is not root:
        children = root.get_children().live()

    # Return the list of values we need to have our template
    # generate the appropriate sidebar HTML.
    return {
        'singleton': singleton,
        'top_level': is_top_page,
        'root': root,
        'current': page,
        'menu_pages': [root] + list(children.in_menu()),
    }
