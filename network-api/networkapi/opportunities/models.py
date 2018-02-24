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


class ImageTextBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    image = ImageChooserBlock()
    ordering = blocks.ChoiceBlock(
        choices=[
            ('left', 'Image on the left'),
            ('right', 'Image on the right'),
        ],
        default='left',
    )

    class Meta:
        icon = 'doc-full'
        template = 'opportunities/blocks/image_text_block.html'


class BiographyBlock(ImageTextBlock):
    name = blocks.CharBlock()

    class Meta:
        icon = 'doc-full'
        template = 'opportunities/blocks/biography_block.html'


class VerticalSpacerBlock(blocks.StructBlock):
    rem = blocks.IntegerBlock()

    class Meta:
        icon = 'arrows-up-down'
        template = 'opportunities/blocks/vertical_spacer_block.html'
        help_text = 'the number of "rem" worth of vertical spacing'


"""
We'll need to figure out which components are truly "base" and
which are bits that should be used in subclassing template-based
page types.
"""
base_fields = [
    ('heading', blocks.CharBlock()),

    ('paragraph', blocks.RichTextBlock()),

    ('image_text', ImageTextBlock()),

    ('image', ImageChooserBlock()),

    ('bio', BiographyBlock()),

    ('video', EmbedBlock()),

    ('linkbutton', LinkButtonBlock()),

    ('spacer', VerticalSpacerBlock()),
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

    def get_context(self, request):
        """
        We use this "enriched" context so that we can easily
        build a menu in the opportunities template based on
        whether this is a singleton opportunity or a mini-site.
        """
        context = super(OpportunityPage, self).get_context(request)
        children = self.get_children()
        has_children = len(children) > 0
        parent = self.get_parent()
        is_top_opportunity = (parent.specific_class != OpportunityPage)
        singleton = is_top_opportunity and not has_children

        context['singleton'] = singleton
        if singleton is False:
            context['top_level'] = is_top_opportunity
            context['child_pages'] = children

        return context
