from django.db import models

from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel, FieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from wagtail.core import blocks
from . import customblocks
from .mixin.foundation_metadata import FoundationMetadataPageMixin
from ..utils import set_main_site_nav_information


class DearInternetPage(FoundationMetadataPageMixin, Page):
    intro_texts = StreamField([
        ('paragraph', blocks.RichTextBlock(
          features=[
              'bold', 'italic', 'link',
          ]
        ))
      ],
    )

    letters_section_heading = models.CharField(
        max_length=300,
        default='Stories from around the world',
    )

    letters = StreamField([
        ('letters', customblocks.DearInternetLetterBlock()),
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

    zen_nav = True

    def get_context(self, request):
        context = super().get_context(request)
        return set_main_site_nav_information(self, context, 'Homepage')

    template = 'wagtailpages/pages/dear_internet_page.html'
