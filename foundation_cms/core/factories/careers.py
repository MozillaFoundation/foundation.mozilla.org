from wagtail import models as wagtail_models

from foundation_cms.base.utils.helpers import to_streamfield_value
from foundation_cms.core.models import GeneralPage

CAREERS_SLUG = "careers"


def build_body(page):
    return to_streamfield_value(
        [
            {
                "type": "title_block",
                "value": {"title": "Work with us", "style": "shape"},
            },
            {
                "type": "greenhouse_board",
                "value": {
                    "empty_heading": "No open roles right now",
                    "empty_description": "<p>We don't have any openings at the moment. Please check back soon.</p>",
                    "unavailable_heading": "Our job board is temporarily unavailable",
                    "unavailable_description": "<p>We're having trouble loading our open roles. "
                    "Please try again shortly.</p>",
                    "hosted_board_notice": "Not seeing our open roles?",
                    "hosted_board_link_label": "View them on Greenhouse",
                },
            },
        ],
        stream_block=page.body.stream_block,
    )


def generate(parent):
    default_locale = wagtail_models.Locale.get_default()

    # Scoped to this parent so a Careers page elsewhere in the tree, in another
    # site or another locale, is neither reused nor touched.
    existing = GeneralPage.objects.child_of(parent).filter(slug=CAREERS_SLUG, locale=default_locale).first()
    if existing:
        if not existing.live:
            existing.save_revision().publish()
        return existing

    page = GeneralPage(
        title="Careers",
        slug=CAREERS_SLUG,
        seo_title="Careers at Mozilla Foundation",
        search_description="Open roles at Mozilla Foundation.",
        locale=default_locale,
        # Off so this fixture does not need hero media to validate.
        show_hero=False,
    )
    page.body = build_body(page)

    parent.add_child(instance=page)
    page.save_revision().publish()
    return page
