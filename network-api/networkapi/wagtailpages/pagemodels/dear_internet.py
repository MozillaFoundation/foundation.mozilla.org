from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from . import customblocks
from .mixin.foundation_metadata import FoundationMetadataPageMixin
from ..utils import set_main_site_nav_information


class DearInternetPage(FoundationMetadataPageMixin, Page):
    intro_text_1 = models.CharField(
        max_length=500,
        help_text='Intro text 1',
    )

    intro_text_2 = models.CharField(
        max_length=500,
        help_text='Intro text 2',
    )

    intro_text_3 = models.CharField(
        max_length=500,
        help_text='Intro text 3',
    )

    intro_text_4 = models.CharField(
        max_length=500,
        help_text='Intro text 4',
    )

    letters = StreamField([
        ('letters', customblocks.DearInternetLetterBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('intro_text_1'),
        FieldPanel('intro_text_2'),
        FieldPanel('intro_text_3'),
        FieldPanel('intro_text_4'),
        StreamFieldPanel('letters'),
    ]

    zen_nav = True

    def get_context(self, request):
        context = super().get_context(request)
        return set_main_site_nav_information(self, context, 'Homepage')

    template = 'wagtailpages/pages/dear_internet_page.html'
