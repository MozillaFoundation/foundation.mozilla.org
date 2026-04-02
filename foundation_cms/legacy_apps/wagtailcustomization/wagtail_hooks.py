from functools import lru_cache

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from wagtail import hooks
from wagtail.models import get_page_models

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

    # get_page_models() returns all concrete page models registered with Wagtail
    all_page_models = get_page_models()

    # Filter down to only the ones that live in legacy apps
    legacy_page_models = [
        model for model in all_page_models
        if model.__module__.startswith(LEGACY_PAGE_MODULE_PREFIXES)
    ]

    if not legacy_page_models:
        return frozenset()

    # Fetch their ContentTypes from the DB and return just the IDs
    legacy_content_types = ContentType.objects.get_for_models(*legacy_page_models)
    legacy_content_type_ids = frozenset(ct.id for ct in legacy_content_types.values())

    return legacy_content_type_ids


@hooks.register("before_edit_page")
def restrict_legacy_page_editing(request, page):
    """Block non-authorized users from editing legacy pages."""
    # Check if this page is a legacy page type using the cached ContentType IDs
    if page.content_type_id in _get_legacy_page_content_type_ids():
        if not is_legacy_authorized(request.user):
            messages.error(request, "You do not have permission to edit this page.")
            return redirect(reverse("wagtailadmin_home"))


@hooks.register("construct_explorer_page_queryset")
def filter_legacy_pages_from_explorer(parent_page, pages, request):
    """Hide legacy pages from the page explorer for non-authorized users."""
    # Authorized users see everything
    if is_legacy_authorized(request.user):
        return pages

    # Exclude legacy pages from the queryset so they don't appear in the explorer
    legacy_ct_ids = _get_legacy_page_content_type_ids()
    if legacy_ct_ids:
        pages = pages.exclude(content_type_id__in=legacy_ct_ids)

    return pages
