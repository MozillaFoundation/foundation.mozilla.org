"""
Wagtail hook registrations for this app.

Wagtail discovers hooks by importing a module named exactly `wagtail_hooks` from
each installed app, so this file cannot take the `wagtail_localize_` prefix its
contents otherwise would. The prefixed names below carry it instead.
"""

from wagtail import hooks

from foundation_cms.base.wagtail_localize_aliases import create_aliases_for_page

WAGTAIL_LOCALIZE_PACKAGE = "wagtail_localize"


def wagtail_localize_handles_copy():
    """
    Safety check if upstream handles the copy. For if wagtail_localize attempts
    to hook / fix the alias clone issue themselves.

    Matches the package and any module inside it, so it still holds if upstream
    moves the hook out of `synctree`. Our own `wagtail_localize_`-prefixed
    modules live under `foundation_cms.` and cannot match by accident.
    """
    return any(
        hook.__module__ == WAGTAIL_LOCALIZE_PACKAGE or hook.__module__.startswith(f"{WAGTAIL_LOCALIZE_PACKAGE}.")
        for hook in hooks.get_hooks("after_copy_page")
    )


# Trigger alias creation after a page is copied
@hooks.register("after_copy_page")
def wagtail_localize_create_aliases_for_copied_page(request, page, new_page):
    """Give a copied page its fallbacks now. Descendants are left to the sync-locale-tree cron."""
    if wagtail_localize_handles_copy():
        return

    create_aliases_for_page(new_page.specific)
