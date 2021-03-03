from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail_localize.fields import SynchronizedField

from . import customblocks
from .mixin.foundation_metadata import FoundationMetadataPageMixin
from ..utils import set_main_site_nav_information


class YoutubeRegretsPage(FoundationMetadataPageMixin, Page):
    headline = models.CharField(
        max_length=500,
        help_text='Page headline',
        blank=True,
    )

    intro_text = StreamField([
        ('text', blocks.CharBlock()),
    ])

    intro_images = StreamField([
        ('image', customblocks.ImageBlock()),
    ])

    faq = StreamField(
        [
            ('paragraph', blocks.RichTextBlock(
                features=[
                    'bold', 'italic',
                    'h2', 'h3', 'h4', 'h5',
                    'ol', 'ul',
                    'link', 'hr',
                ]
            ))
        ],
        blank=True,
    )

    regret_stories = StreamField([
        ('regret_story', customblocks.YoutubeRegretBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('headline'),
        StreamFieldPanel('intro_text'),
        StreamFieldPanel('intro_images'),
        StreamFieldPanel('faq'),
        StreamFieldPanel('regret_stories'),
    ]

    zen_nav = True

    override_translatable_fields = [
        SynchronizedField('slug'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        return set_main_site_nav_information(self, context, 'Homepage')

    template = 'wagtailpages/pages/youtube_regrets_page.html'


class YoutubeRegretsReporterPage(FoundationMetadataPageMixin, Page):
    headline = models.CharField(
        max_length=500,
        help_text='Page headline',
        blank=True,
    )

    intro_text = StreamField([
        ('text', blocks.CharBlock()),
    ])

    intro_images = StreamField([
        ('image', customblocks.ImageBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('headline'),
        StreamFieldPanel('intro_text'),
        StreamFieldPanel('intro_images'),
    ]

    zen_nav = True

    override_translatable_fields = [
        SynchronizedField('slug'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        return set_main_site_nav_information(self, context, 'Homepage')

    template = 'wagtailpages/pages/youtube_regrets_reporter_page.html'
