from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail_localize.fields import SynchronizedField, TranslatableField

from . import customblocks
from .base import BasePage
from .customblocks import LinkBlock
from .customblocks.base_rich_text_options import base_rich_text_options


class DearInternetPage(BasePage):
    intro_texts = StreamField(
        [("intro_text", blocks.RichTextBlock(features=base_rich_text_options))], use_json_field=True
    )

    letters_section_heading = models.CharField(
        max_length=300,
        default="Stories from around the world",
    )

    letters = StreamField(
        [
            ("letter", customblocks.DearInternetLetterBlock()),
        ],
        use_json_field=True,
    )

    cta = models.CharField(
        max_length=500,
    )

    cta_button_text = models.CharField(
        max_length=100,
    )

    cta_button_link = models.URLField()

    cta_button = StreamField([("link", LinkBlock())], use_json_field=True, blank=True, max_num=1,)

    content_panels = Page.content_panels + [
        FieldPanel("intro_texts"),
        FieldPanel("letters_section_heading"),
        FieldPanel("letters"),
        MultiFieldPanel(
            [
                FieldPanel("cta"),
                FieldPanel("cta_button"),
            ],
            heading="CTA",
        ),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields
        TranslatableField("title"),
        TranslatableField("intro_texts"),
        TranslatableField("letters_section_heading"),
        TranslatableField("letters"),
        TranslatableField("cta"),
        TranslatableField("cta_button"),
    ]

    template = "wagtailpages/pages/dear_internet_page.html"
