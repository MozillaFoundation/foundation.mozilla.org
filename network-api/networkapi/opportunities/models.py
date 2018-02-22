from django.db import models

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

base_fields = [
    ('heading', blocks.CharBlock(classname="full title")),

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
    body = StreamField(base_fields)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


class OpportunityPage(ModularPage):
    pass
