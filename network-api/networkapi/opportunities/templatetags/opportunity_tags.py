from django import template

register = template.Library()


# Retrieves all live pages which are children of the calling page for standard index listing
@register.inclusion_tag('opportunities/tags/child_listing.html', takes_context=True)
def child_listing(context, calling_page):
    pages = calling_page.get_children().live().in_menu()
    return {
        'pages': pages,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }