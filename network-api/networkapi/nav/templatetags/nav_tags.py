from django import template

from networkapi.wagtailpages.models import Homepage

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
def check_if_dropdown_is_active(context, dropdown_id):
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

    # If that didn't work, let's check if the page is a child of the dropdown's CTA button page link
    dropdown_link_page_path = dropdowns_page_links[dropdown_id][dropdown_link_page_id]
    if page.path.startswith(dropdown_link_page_path):
        return True

    # Finally, let's check if the page is a child of any of the page links inside the dropdown
    for id in dropdowns_page_links[dropdown_id]["page_ids"]:
        link_path = dropdowns_page_links[dropdown_id][id]
        if page.path.startswith(link_path):
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
    if page == link_page:
        return True

    # Check if the current page is a child of the linked page
    if page.path.startswith(link_page.path):
        return True

    return False
