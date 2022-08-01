from django import http
from django.db import models
from wagtail import images
from wagtail.admin import edit_handlers as panels
from wagtail.core import blocks, fields
from wagtail.core import models as wagtail_models
from wagtail.images import edit_handlers as image_panels

from networkapi.wagtailpages.pagemodels import customblocks
from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class BuyersGuideArticlePage(
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page
):
    parent_page_types = ['wagtailpages.BuyersGuideEditorialContentIndexPage']
    subpage_types = []
    template = 'pages/buyersguide/article_page.html'

    hero_image = models.ForeignKey(
        images.get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Image for the hero section of the page.',
    )
    body = fields.StreamField(
        block_types=(
            ('accordion', customblocks.AccordionBlock()),
            ('paragraph', blocks.RichTextBlock(
                features=customblocks.full_content_rich_text_options,
                template='wagtailpages/blocks/rich_text_block.html',
            )),
            ('card_grid', customblocks.CardGridBlock()),
            ('image_grid', customblocks.ImageGridBlock()),
            ('iframe', customblocks.iFrameBlock()),
            ('image', customblocks.AnnotatedImageBlock()),
            ('audio', customblocks.AudioBlock()),
            ('image_text', customblocks.ImageTextBlock()),
            ('image_text_mini', customblocks.ImageTextMini()),
            ('video', customblocks.VideoBlock()),
            ('linkbutton', customblocks.LinkButtonBlock()),
            ('looping_video', customblocks.LoopingVideoBlock()),
            ('pulse_listing', customblocks.PulseProjectList()),
            ('single_quote', customblocks.SingleQuoteBlock()),
            ('slider', customblocks.FoundationSliderBlock()),
            ('spacer', customblocks.BootstrapSpacerBlock()),
            ('airtable', customblocks.AirTableBlock()),
            ('datawrapper', customblocks.DatawrapperBlock()),
            ('typeform', customblocks.TypeformBlock()),
        ),
        block_counts={'typeform': {'max_num': 1}},
        null=True,
        blank=False,
    )

    content_panels = wagtail_models.Page.content_panels + [
        image_panels.ImageChooserPanel('hero_image'),
        panels.StreamFieldPanel('body'),
    ]

    def get_context(self, request: http.HttpRequest, *args, **kwargs) -> dict:
        context = super().get_context(request, *args, **kwargs)
        context['home_page'] = self.get_parent().get_parent().specific
        return context
