from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from networkapi.wagtailpages.utils import get_page_tree_information
from networkapi.wagtailpages.models import (
    base_fields,
    FoundationMetadataPageMixin
)


class MozfestPrimaryPage(FoundationMetadataPageMixin, Page):
    header = models.CharField(
        max_length=250,
        blank=True
    )

    banner = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='mozfest_primary_banner',
        verbose_name='Hero Image',
        help_text='Choose an image that\'s bigger than 4032px x 1152px with aspect ratio 3.5:1',
    )

    intro = models.CharField(
        max_length=250,
        blank=True,
        help_text='Intro paragraph to show in hero cutout box'
    )

    body = StreamField(base_fields)

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        ImageChooserPanel('banner'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'MozfestPrimaryPage',
    ]

    show_in_menus_default = True

    def get_context(self, request):
        context = super().get_context(request)
        return get_page_tree_information(self, context)


class MozfestHomepage(MozfestPrimaryPage):
    banner_heading = models.CharField(
        max_length=250,
        blank=True,
        help_text='A banner heading specific to the homepage'
    )

    banner_guide_text = models.CharField(
        max_length=1000,
        blank=True,
        help_text='A banner paragraph specific to the homepage'
    )

    banner_video_url = models.URLField(
        max_length=2048,
        blank=True,
        help_text='The video to play when users click "watch video"'
    )

    subpage_types = [
        'MozfestPrimaryPage'
    ]

    content_panels = MozfestPrimaryPage.content_panels + [
        FieldPanel('banner_heading'),
        FieldPanel('banner_guide_text'),
        FieldPanel('banner_video_url'),
    ]
