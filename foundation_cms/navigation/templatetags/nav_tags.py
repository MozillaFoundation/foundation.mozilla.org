from django import template

from foundation_cms.legacy_apps.wagtailpages.models import (
    BlogIndexPage,
    BlogPage,
    Homepage,
)

register = template.Library()


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
