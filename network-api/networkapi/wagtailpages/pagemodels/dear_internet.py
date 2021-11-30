from django.db import models

from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel, FieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from wagtail_localize.fields import SynchronizedField, TranslatableField

from wagtail.core import blocks
from .base_fields import base_rich_text_options
from . import customblocks
from .mixin.foundation_metadata import FoundationMetadataPageMixin
from ..utils import set_main_site_nav_information


class DearInternetPage(FoundationMetadataPageMixin, Page):
    intro_texts = StreamField([
        ('intro_text', blocks.RichTextBlock(
        features=(base_rich_text_options)
        ))
      ],
    )

    letters_section_heading = models.CharField(
        max_length=300,
        default='Stories from around the world',
    )

    letters = StreamField([
        ('letter', customblocks.DearInternetLetterBlock()),
    ])

    cta = models.CharField(
        max_length=500,
    )

    cta_button_text = models.CharField(
        max_length=100,
    )

    cta_button_link = models.URLField()

    content_panels = Page.content_panels + [
        StreamFieldPanel('intro_texts'),
        FieldPanel('letters_section_heading'),
        StreamFieldPanel('letters'),
        MultiFieldPanel(
            [
                FieldPanel('cta'),
                FieldPanel('cta_button_text'),
                FieldPanel('cta_button_link'),
            ],
            heading='CTA',
        ),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField('title'),
        TranslatableField('intro_texts'),
        TranslatableField('letters_section_heading'),
        TranslatableField('letters'),
        TranslatableField('cta'),
        TranslatableField('cta_button_text'),
        SynchronizedField('cta_button_link'),
    ]

    zen_nav = True

    def get_context(self, request):
        context = super().get_context(request)
        return set_main_site_nav_information(self, context, 'Homepage')

    template = 'wagtailpages/pages/dear_internet_page.html'
