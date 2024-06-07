from django import template

from networkapi.wagtailpages.models import BlogIndexPage, BlogPage, Homepage

register = template.Library()


# Instantiate a horizontal nav based on the current page's relation to other pages
@register.inclusion_tag("tags/horizontal_nav.html", takes_context=True)
def horizontal_nav(context, current_page, menu_pages, classname=""):
    return {
        "current": current_page,
        "menu_pages": menu_pages,
        "classname": classname,
    }


@register.simple_tag
def get_dropdown_id(**kwargs):
    try:
        index = int(kwargs["idx"])
    except ValueError:
        return None
    menu = kwargs.get("menu", None)
    if not menu:
        return None
    return menu.dropdowns.get_prep_value()[index]["id"]


@register.simple_tag(takes_context=True)
def check_if_dropdown_can_be_active(context, dropdown_id):
    # The page that user is currently visiting/requesting:
    page = context.get("page", None)
    if not page:
        return None
    menu = context.get("menu", None)
    if not menu:
        return None
    dropdowns_page_links = menu.page_references_per_dropdown

    # Don't highlight the link if the page is the homepage
    if isinstance(page, Homepage):
        return False

    dropdown_link_page_id = dropdowns_page_links[dropdown_id]["self_page_id"]
    # If the dropdown doesn't have a CMS page link (external/relative/etc), we can't
    # get the page's request to properly check if the dropdown is active:
    if not dropdown_link_page_id:
        return False

    # Check if page is in the dropdown's links (even if it's not a direct child):
    if page.id in dropdowns_page_links[dropdown_id]["page_ids"]:
        return True

    return False


@register.simple_tag(takes_context=True)
def check_if_blog_dropdown_can_be_active(context):
    """
    Check if the blog dropdown can be highlighted based on the current page.
    Unlike other dropdowns, we don't need to check the current page against the dropdown's links.
    For blog dropdown, all we need to check is if the current page is a blog index page or a blog page.
    """

    # The page that user is currently visiting/requesting:
    page = context.get("page", None)
    if not page:
        return None

    # Highlight the dropdown if the page is a blog index page (e.g., the main blog index or any blog topic page)
    if isinstance(page, BlogIndexPage):
        return True

    # Highlight the dropdown if the page is a blog page
    if isinstance(page, BlogPage):
        return True

    return False


@register.simple_tag(takes_context=True)
def check_if_link_is_active(context, link):
    # False if the link is not to a page (external/relative/etc)
    if link["link_to"] != "page":
        return False
    if not link["page"]:
        return False

    # Page that the user is currently visiting/requesting:
    page = context.get("page", None)
    if not page:
        return None

    # Don't highlight the link if the page is the homepage
    if isinstance(page, Homepage):
        return False

    link_page = link["page"]

    # Check if the current page is the linked page
    if page.id == link_page.id:
        return True

    return False
