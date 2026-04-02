from functools import lru_cache

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from wagtail import hooks
from wagtail.models import Page

from foundation_cms.legacy_apps.wagtailcustomization.permissions import is_legacy_authorized

# Explicit list of legacy app module prefixes whose pages should be restricted.
# Mozfest pages are intentionally excluded as access is managed via the CMS page tree.
LEGACY_PAGE_MODULE_PREFIXES = (
    "foundation_cms.legacy_apps.wagtailpages.",
    "foundation_cms.legacy_apps.donate.",
    "foundation_cms.legacy_apps.donate_banner.",
)


@lru_cache(maxsize=None)
def _get_legacy_page_content_type_ids():
    """
    Return a frozenset of ContentType IDs for all restricted legacy page types.
    Result is cached after the first call since page types don't change at runtime.
    """
    from django.contrib.contenttypes.models import ContentType

    legacy_models = []
    stack = list(Page.__subclasses__())
    while stack:
        cls = stack.pop()
        if cls.__module__.startswith(LEGACY_PAGE_MODULE_PREFIXES):
            legacy_models.append(cls)
        stack.extend(cls.__subclasses__())

    if not legacy_models:
        return frozenset()

    content_types = ContentType.objects.get_for_models(*legacy_models)
    return frozenset(ct.id for ct in content_types.values())


@hooks.register("before_edit_page")
def restrict_legacy_page_editing(request, page):
    """Block non-authorized users from editing legacy pages."""
    if page.__class__.__module__.startswith(LEGACY_PAGE_MODULE_PREFIXES):
        if not is_legacy_authorized(request.user):
            messages.error(request, "You do not have permission to edit this page.")
            return redirect(reverse("wagtailadmin_home"))


@hooks.register("construct_explorer_page_queryset")
def filter_legacy_pages_from_explorer(parent_page, pages, request):
    """Hide legacy pages from the page explorer for non-authorized users."""
    if is_legacy_authorized(request.user):
        return pages
    legacy_ct_ids = _get_legacy_page_content_type_ids()
    if legacy_ct_ids:
        pages = pages.exclude(content_type_id__in=legacy_ct_ids)
    return pages
