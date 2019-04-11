from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    altText = blocks.CharBlock(
        required=True,
        help_text='Image description (for screen readers).'
    )

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/image_block.html'


class ImageTextBlock(ImageBlock):
    text = blocks.RichTextBlock(
        features=['bold', 'italic', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'link']
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
            divider_styles.append('div-top')
        if value.get("bottom_divider"):
            divider_styles.append('div-bottom')
        context['divider_styles'] = ' '.join(divider_styles)
        return context

    class Meta:
        icon = 'doc-full'
        template = 'wagtailpages/blocks/image_text.html'
