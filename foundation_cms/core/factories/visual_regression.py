"""Small, deterministic fixtures for the redesign visual regression suite."""

from django.db import transaction
from wagtail.models import Page

from foundation_cms.base.utils.helpers import to_streamfield_value
from foundation_cms.core.models import GeneralPage


def populated_body():
    # These are the components available on site-refresh-2026. Their existing
    # styles are exercised without depending on unmerged component reskins.
    return [
        {
            "type": "section_start",
            "value": {
                "name": "Visual regression components",
                "anchor_id": "visual-components",
                "rhythm": "xlarge",
                "padding": "large",
                "divider": False,
            },
        },
        {"type": "rich_text", "value": "<p>A small, stable page for reviewing the Cosmos reskin.</p>"},
        *[
            {
                "type": "link_button_block",
                "value": {
                    "label": label,
                    "link_to": "relative_url",
                    "relative_url": "/en/visual-regression-empty/",
                    "style": style,
                    "alignment": "link-button-block--left",
                    "new_window": False,
                },
            }
            for label, style in [("Explore the empty page", "btn-primary"), ("View the page shell", "btn-secondary")]
        ],
        {
            "type": "accordion_block",
            "value": {
                "accordion_items": [
                    {
                        "title": "What does this page cover?",
                        "content": [
                            {"type": "rich_text", "value": "<p>Page layout, links and accordion content.</p>"}
                        ],
                    },
                    {
                        "title": "Why use fixed content?",
                        "content": [
                            {
                                "type": "rich_text",
                                "value": "<p>Stable content makes visual changes easier to review.</p>",
                            }
                        ],
                    },
                ]
            },
        },
    ]


@transaction.atomic
def generate(parent):
    """Create missing pages only; never replace or republish existing content."""
    pages = []
    for slug, title, body in [
        ("visual-regression-empty", "Visual regression: empty page", []),
        ("visual-regression-components", "Visual regression: components", populated_body()),
    ]:
        existing = Page.objects.child_of(parent).filter(slug=slug, locale=parent.locale).first()
        if existing:
            if not isinstance(existing.specific, GeneralPage):
                raise ValueError(f"Refusing to reuse a non-GeneralPage at {slug}.")
            if not existing.live:
                raise ValueError(
                    f"Visual fixture {slug} is unpublished. Review and publish it manually before retrying; "
                    "existing content has been left unchanged."
                )
            pages.append(existing.specific)
            continue

        page = GeneralPage(
            title=title,
            seo_title=title,
            slug=slug,
            locale=parent.locale,
            theme="default",
            search_description="Deterministic redesign visual regression fixture.",
            show_hero=False,
        )
        page.body = to_streamfield_value(body, stream_block=page.body.stream_block)
        parent.add_child(instance=page)
        page.save_revision().publish()
        pages.append(page)
    return pages
