from wagtail.core import blocks
from .image_block import ImageBlock
from ..customblocks.base_rich_text_options import base_rich_text_options


class ImageTextBlock(ImageBlock):
    text = blocks.RichTextBlock(
        features=base_rich_text_options + ['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul']
    )
    url = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this image should link out to.',
    )
    top_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider above content block.',
    )
    bottom_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider below content block.',
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        divider_styles = []
        if value.get("top_divider"):
            divider_styles.append('div-top pt-4')
        if value.get("bottom_divider"):
            divider_styles.append('div-bottom pb-4')
        context['divider_styles'] = ' '.join(divider_styles)
        return context

    class Meta:
        icon = 'doc-full'
        template = 'wagtailpages/blocks/image_text.html'
