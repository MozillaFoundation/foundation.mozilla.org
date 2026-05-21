from django.db import models
from django.forms import ValidationError
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_general_page import (
    AbstractGeneralPage,
    general_page_block_options,
)
from foundation_cms.blocks import LinkBlock
from foundation_cms.core.panels.media_panel import MediaPanel
from foundation_cms.mixins.hero_media import HeroMediaMixin


class GeneralPage(AbstractGeneralPage, HeroMediaMixin):

    show_hero = models.BooleanField(
        default=True,
        verbose_name="Show Hero Section",
        help_text="Check to display the hero section on this page.",
    )

    hero_description = models.CharField(
        max_length=120,
        help_text="Hero Description",
        blank=True,
    )

    hero_variant = models.CharField(
        max_length=50,
        choices=[
            ("side-by-side", "Side by Side"),
            ("top-to-bottom", "Top to Bottom"),
        ],
        default="side-by-side",
        help_text="Select the variant of the hero section",
    )

    hero_background_color = models.CharField(
        max_length=50,
        choices=[
            ("orange-200", "Orange"),
            ("yellow-200", "Yellow"),
        ],
        blank=True,
        default="",
        help_text="Select the color of the hero background, only for 'Top to Bottom' variant.",
    )

    hero_media_rounded_corners = models.BooleanField(
        default=True,
        verbose_name="Hero Media Rounded Corners",
        help_text=(
            "By default, rounded corners are applied "
            "(top-right corner for 'Side by Side', both top corners for 'Top to Bottom'). "
            "Uncheck to remove rounded corners."
        ),
    )

    hero_cta_link = StreamField(
        [("button", LinkBlock())],
        use_json_field=True,
        blank=True,
        max_num=1,
        verbose_name="Button",
    )

    body = StreamField(
        general_page_block_options,
        block_counts={"donor_help_contact_us_form": {"max_num": 1}},
        use_json_field=True,
        blank=True,
    )

    content_panels = [
        FieldPanel("title"),
        MultiFieldPanel(
            [
                FieldPanel("show_hero"),
                MediaPanel(
                    [
                        FieldPanel("hero_variant"),
                        FieldPanel(
                            "hero_background_color",
                            attrs={"data-media-target": "field", "data-condition": "top-to-bottom"},
                        ),
                    ],
                    trigger_field="hero_variant",
                ),
                FieldPanel("hero_title"),
                FieldPanel("hero_description"),
                MediaPanel(
                    [
                        FieldPanel("displayed_hero_content"),
                        FieldPanel(
                            "hero_image",
                            attrs={"data-media-target": "field", "data-condition": HeroMediaMixin.HERO_CONTENT_IMAGE},
                        ),
                        FieldPanel(
                            "hero_image_alt_text",
                            attrs={"data-media-target": "field", "data-condition": HeroMediaMixin.HERO_CONTENT_IMAGE},
                        ),
                        FieldPanel(
                            "hero_video_url",
                            attrs={"data-media-target": "field", "data-condition": HeroMediaMixin.HERO_CONTENT_VIDEO},
                        ),
                    ],
                    trigger_field="displayed_hero_content",
                ),
                FieldPanel("hero_media_rounded_corners"),
                FieldPanel("hero_cta_link"),
            ],
            heading="Hero Section",
            classname="collapsible",
        ),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractGeneralPage.translatable_fields + [
        # Content tab fields
        SynchronizedField("show_hero"),
        SynchronizedField("hero_variant"),
        SynchronizedField("hero_background_color"),
        TranslatableField("hero_title"),
        TranslatableField("hero_description"),
        SynchronizedField("hero_image"),
        SynchronizedField("hero_media_rounded_corners"),
        SynchronizedField("displayed_hero_content"),
        SynchronizedField("hero_video_url"),
        TranslatableField("hero_image_alt_text"),
        TranslatableField("hero_cta_link"),
        TranslatableField("body"),
    ]

    search_fields = AbstractGeneralPage.search_fields + [
        index.SearchField("body", boost=6),
        index.SearchField("hero_title", boost=4),
        index.SearchField("hero_description", boost=4),
        index.SearchField("hero_image_alt_text", boost=2),
    ]

    class Meta:
        verbose_name = "General Page"

    def clean(self):
        super().clean()
        errors = {}

        if self.hero_variant == "side-by-side":
            self.hero_background_color = ""

        if self.hero_variant == "top-to-bottom" and not self.hero_background_color:
            errors["hero_background_color"] = "Background color is required when variant is 'Top to Bottom'."

        if errors:
            raise ValidationError(errors)

    # keep an explicit fallback in case no themed templates exist
    template = "patterns/pages/core/general_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Checking if a Donor contact us form block is present in the page body.
        # If one is, we will render the template formassembly_head.hml which includes
        # the necessary JS for the form.
        if any(block.block_type == "donor_help_contact_us_form" for block in self.body):
            context["has_donor_contact_us_form"] = True
        return context
