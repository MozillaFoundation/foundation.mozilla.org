"""
Fills a gap in wagtail-localize: locale fallback ("alias") creation on page copy.

wagtail-localize creates aliases from its `after_create_page` hook only, which
fires for the "add page" form and nothing else. Copying a page goes through
`after_copy_page`, so a clone is reachable in the default locale and nowhere
else until the hourly `sync_locale_trees` cron catches up.

Everything here exists solely because of that upstream gap. The
`wagtail_localize_` prefix on this module marks it as deletable in one go if
upstream closes it -- see the guards in wagtail_hooks.py.
"""

import logging

from wagtail.models import Locale, Page
from wagtail_localize.models import LocaleSynchronization

logger = logging.getLogger(__name__)


def create_aliases_for_page(page):
    """
    Create alias pages for page in every locale that syncs from its locale.
    """
    if page.alias_of_id is not None:
        # An alias is somebody else's fallback, not new content of its own.
        return []

    occupied_locale_ids = Page.objects.filter(translation_key=page.translation_key).values_list("locale_id", flat=True)
    target_locales = Locale.objects.filter(
        id__in=LocaleSynchronization.objects.filter(sync_from=page.locale).values_list("locale_id", flat=True)
    ).exclude(id__in=occupied_locale_ids)

    created = []

    for locale in target_locales:
        try:
            created.append(page.copy_for_translation(locale, copy_parents=True, alias=True))
        except Exception:
            logger.exception(
                "Could not create a %s locale fallback for page %s (id=%s); sync_locale_trees will retry it",
                locale.language_code,
                page.slug,
                page.pk,
            )

    return created
