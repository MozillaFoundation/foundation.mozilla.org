from django.db import models

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock


class LinkButtonBlock(blocks.StructBlock):
    label = blocks.CharBlock()
    URL = blocks.URLBlock()

    class Meta:
        icon = 'link'
        template = 'opportunities/blocks/link_button_block.html'

"""
We'll need to figure out which components are truly "base" and
which are bits that should be used in subclassing template-based
page types.
"""
base_fields = [
    ('heading', blocks.CharBlock()),

    ('paragraph', blocks.RichTextBlock()),

    ('image+text', blocks.StructBlock([
        ('text', blocks.CharBlock()),
        ('image', ImageChooserBlock()),
    ], icon='doc-full')),

    ('text+image', blocks.StructBlock([
        ('picture', ImageChooserBlock()),
        ('text', blocks.CharBlock()),
    ], icon='doc-full')),

    ('image', ImageChooserBlock()),

    ('bio', blocks.StructBlock([
        ('name', blocks.CharBlock()),
        ('bio', blocks.TextBlock()),
        ('picture', ImageChooserBlock()),
    ])),

    ('video', EmbedBlock()),

    ('linkbutton', LinkButtonBlock())
]

class ModularPage(Page):
    """
    The base class offers universal component picking
    """

    header = models.CharField(
        max_length=250,
        blank=True
    )

    body = StreamField(base_fields)

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        StreamFieldPanel('body'),
    ]


class OpportunityPage(ModularPage):
    """
    For now, the opportunity pages are just a form of
    modular page type, with CSS classes defined in the
    opportunities/templates/opportunities/opportunity_page.html
    template file.
    """
    pass
