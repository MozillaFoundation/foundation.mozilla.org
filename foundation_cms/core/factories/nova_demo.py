from uuid import uuid4

from django.core.management.base import CommandError
from django.db import transaction
from wagtail.models import Site

from foundation_cms.core.factories.general_page import GeneralPageFactory
from foundation_cms.core.models import GeneralPage


def demo_body():
    return [
        {
            "type": "rich_text",
            "value": (
                "<h2>Rich text: default block fallback</h2><p>Identical content on both pages. "
                "Nova changes the page, navigation, breadcrumbs, quote and footer templates; "
                "this rich-text block keeps its existing template.</p>"
            ),
        },
        {
            "type": "quote",
            "value": {
                "quote": ("Nova moves the attribution before the quote. Default keeps the original block structure."),
                "attribution": "Quote block override",
            },
        },
        {
            "type": "two_column_container_block",
            "value": {
                "background_color": "white",
                "vertical_alignment": "top",
                "left_column": [
                    {
                        "id": str(uuid4()),
                        "type": "quote",
                        "value": {
                            "quote": "This quote inherits the page theme inside an unchanged two-column container.",
                            "attribution": "Nested quote override",
                        },
                    }
                ],
                "right_column": [
                    {
                        "id": str(uuid4()),
                        "type": "rich_text",
                        "value": (
                            "<h2>Two-column container: default fallback</h2><p>The container and this rich-text block "
                            "keep their existing templates. The nested quote uses the Nova override.</p>"
                        ),
                    }
                ],
            },
        },
    ]


@transaction.atomic
def generate():
    """Create demo pages that do not already exist."""
    site = Site.objects.filter(is_default_site=True).first()
    if not site:
        raise CommandError("A default site is required; no site or content was changed.")

    def create(parent, slug, theme):
        existing = parent.get_children().filter(slug=slug).first()
        if existing:
            if not isinstance(existing.specific, GeneralPage):
                raise CommandError(f"{slug} already belongs to another page type; left unchanged.")
            return existing.specific
        page = GeneralPageFactory.build(
            title="Page template override",
            seo_title="Theme template POC",
            slug=slug,
            locale=parent.locale,
            theme=theme,
            body=demo_body(),
        )
        parent.add_child(instance=page)
        page.save_revision().publish()
        return page

    root = create(site.root_page, "nova-demo", "default")
    default = create(root, "default", "default")
    nova = create(root, "nova", "nova")
    inherited = create(nova, "inherited", "")
    overridden = create(nova, "default-override", "default")
    return [root, default, nova, inherited, overridden]
